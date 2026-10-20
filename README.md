# Plataforma de Gestão Interna Empresarial

Aplicação web para centralizar chamados, tarefas e informações operacionais, com acesso organizado por perfil de usuário. Este repositório contém o frontend em **Reflex (Python)** e os contratos exportados do backend **Xano**.

## Sobre o projeto

A plataforma busca facilitar o registro e o acompanhamento de solicitações, aproximando funcionários, técnicos e gestores em um mesmo fluxo. O sistema diferencia o acesso de funcionários, técnicos, gestores e administradores; as permissões de dados e operações são aplicadas pelo backend Xano.

## Perfis e áreas

- **Funcionário:** abre e acompanha os próprios chamados e consulta/conclui tarefas atribuídas a ele, com solução informada.
- **Técnico:** consulta chamados, pode associar chamados abertos a si, registrar interações e atualizar o atendimento conforme as regras do backend.
- **Gestor:** consulta chamados e organiza usuários e tarefas de acordo com o escopo do seu departamento; o gestor de T.I. tem o escopo administrativo descrito na documentação.
- **Administrador:** dispõe de dashboard global, consultas de chamados e tarefas, cadastro de usuários e consulta/exportação CSV do histórico de interações.

Os portais de funcionário, técnico e gestor permitem as operações descritas em suas respectivas documentações. O portal administrativo mantém chamados e tarefas em modo de consulta; cadastro de usuários e exportação do histórico são áreas separadas.

## Arquitetura

| Parte | Tecnologia | Responsabilidade |
| --- | --- | --- |
| Frontend | Reflex e Python | Interface, navegação por perfil e chamadas autenticadas |
| Backend | Xano | APIs, autenticação, autorização, regras de negócio e persistência |
| Especificação | OpenSpec | Planejamento incremental de requisitos, design e tarefas |

Os arquivos exportados do Xano estão organizados em `apis/`, `functions/`, `tables/` e `database/`. Alterações locais nesses arquivos não são publicadas automaticamente no backend remoto.

## Estado do projeto

O repositório contém a aplicação Reflex, os portais dos quatro perfis e documentação dos fluxos existentes. Os registros do projeto também incluem testes Python locais e validações manuais relatadas para alguns portais.

Isso não significa que todas as verificações estejam concluídas: os registros da mudança administrativa apontam testes autenticados de endpoints Xano que ainda precisam ser executados. Portanto, este README não declara o MVP completo nem a aplicação publicada em produção. Consulte as evidências e pendências na documentação vinculada abaixo.

### Escopo previsto para o MVP

O planejamento geral também prevê gestão de ativos e departamentos, indicadores operacionais e a integração de pelo menos uma funcionalidade de inteligência artificial. Esses itens fazem parte do escopo planejado e não devem ser interpretados, apenas por constarem no plano, como entregas concluídas. A IA é prevista como apoio aos usuários, sem substituir decisões humanas.

## Executar localmente

Os comandos abaixo seguem a configuração documentada para Windows PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Edite `.env` e configure `XANO_API_BASE_URL` com a URL base do grupo de API Authentication do seu ambiente Xano. Não compartilhe nem versione credenciais ou valores privados. Depois, inicie a aplicação:

```powershell
.\.venv\Scripts\reflex.exe run
```

A aplicação usa `/login` para autenticação. O acesso às demais áreas depende de uma sessão validada pelo Xano.

## Documentação

- [Visão geral e escopo inicial](docs/project-overview.md) — documento de concepção do projeto; algumas decisões nele são históricas e podem anteceder a implementação atual.
- [Modelo de domínio](docs/domain-model.md)
- [Autenticação e sessão](docs/login-sessao.md)
- [Portal do funcionário e portal gerencial](docs/portal-gerencial.md)
- [Portal de atendimento técnico](docs/portal-tecnico.md)
- [Portal administrativo](docs/portal-admin.md)
- [Dependências Python](requirements.txt)

## Segurança

Não versione o arquivo `.env`. A autorização efetiva dos dados e das operações deve ser garantida pelo backend Xano, não apenas pela interface. A documentação de sessão registra que o token fica no `LocalStorage` do navegador e descreve o risco associado a esse armazenamento.
