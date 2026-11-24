# Nexo | Gestão Interna

O Nexo é uma aplicação web para abrir e atender chamados internos, distribuir tarefas e gerenciar usuários. A interface é feita em **Reflex (Python)**, o **Xano** autentica usuários e aplica as permissões, e o **n8n** fornece sugestões de solução no atendimento técnico.

## O que cada perfil pode fazer

| Perfil | Funcionalidades |
| --- | --- |
| Funcionário | Abre e acompanha os próprios chamados. Em **Minhas tarefas**, consulta as tarefas atribuídas a ele e registra a solução ao concluí-las. |
| Técnico | Assume chamados abertos, registra interações e atualiza o status e a solução final dos atendimentos sob sua responsabilidade. Também consulta e conclui as próprias tarefas. |
| Gestor | Abre chamados, consulta os chamados do seu departamento, cadastra usuários e cria tarefas para um ou mais responsáveis autorizados. Em **Tarefas criadas**, acompanha as próprias tarefas e consulta a solução registrada. O gestor de T.I. tem consulta global de chamados, escopo ampliado de cadastro e atribui tarefas aos técnicos de T.I. |
| Administrador | Acompanha indicadores no dashboard global, consulta chamados e tarefas, cadastra e edita usuários e exporta o histórico de interações em CSV. |

A busca de chamados permite filtrar por prioridade, status e nome do solicitante dentro do escopo de acesso de cada perfil.

Na tela **Tarefas criadas**, o gestor pode filtrar as tarefas por status e abrir o detalhe para consultar descrição, responsáveis, prioridade, prazo e chamado vinculado. A conclusão feita por um responsável vale para toda a tarefa, e a solução fica visível no detalhe. O prazo usa o formato `DD/MM/AAAA` na interface.

### Sugestão de solução no atendimento

No detalhe de um chamado editável, o técnico autorizado pode selecionar **Sugerir solução**. O Xano verifica a permissão antes de chamar o n8n. O modal **Solução sugerida** mostra os procedimentos retornados e, quando disponível e autorizada, a referência a outro chamado.

O técnico avalia a sugestão e registra a solução final pelo fluxo normal de atendimento. A consulta preserva o rascunho e o status do chamado.

## Executar localmente

No Windows PowerShell, a partir da raiz do repositório:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
if (-not (Test-Path .env)) { Copy-Item .env.example .env }
```

Se já tiver um `.env`, preserve o arquivo existente. Defina `XANO_API_BASE_URL` com a URL base do grupo de APIs **Authentication** do seu ambiente Xano. Use uma conta cadastrada nesse ambiente para acessar o sistema.

```powershell
.\.venv\Scripts\reflex.exe run
```

Abra a URL exibida no terminal. A autenticação fica em `/login`, o portal do perfil em `/` e **Minhas tarefas** em `/tarefas`.

Para usar **Sugerir solução**, o ambiente Xano precisa disponibilizar o endpoint `POST /chamado/{chamado_id}/sugerir-solucao` e ter o fluxo n8n configurado. As variáveis `N8N_SUGGESTION_HEADER_NAME` e `N8N_SUGGESTION_HEADER_VALUE` são configuradas no Xano. Mantenha o `.env` e as credenciais fora do Git.

## Estrutura do repositório

| Caminho | Conteúdo |
| --- | --- |
| [TI_da_Firma/](TI_da_Firma/) | Aplicação Reflex, portais por perfil, estado da sessão e cliente das APIs Xano. |
| [apis/](apis/), [functions/](functions/) e [tables/](tables/) | Definições locais de endpoints, funções e tabelas do Xano. |
| [database/](database/) | Exportações da estrutura do Xano. |
| [openspec/](openspec/) | Especificações e histórico das mudanças. |
| [tests/](tests/) | Testes Python dos portais, das permissões e do cliente Xano. |

## Documentação

- [Autenticação e sessão](docs/login-sessao.md)
- [Portal gerencial e tarefas do funcionário](docs/portal-gerencial.md)
- [Portal de atendimento técnico](docs/portal-tecnico.md)
- [Sugestões de solução via n8n](openspec/changes/sugerir-solucao-chamado-n8n/specs/ticket-solution-suggestions/spec.md)
- [Portal administrativo](docs/portal-admin.md)
- [Modelo de domínio](docs/domain-model.md)
- [Visão geral e planejamento inicial](docs/project-overview.md)
