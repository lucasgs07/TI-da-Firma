<!-- reflex managed begin (do not edit inside this block; add custom content outside the markers) -->
# Agents

This project uses the **Reflex agent skills** � up-to-date knowledge for building full-stack Python web apps with [Reflex](https://reflex.dev). Install them first, then use them as described below.

## Installing the Skills

Before working on this project, make sure the Reflex skills are available to you.

### Claude Code

If the skills are not already available, install them yourself by running these shell commands:

```bash
claude plugin marketplace add reflex-dev/agent-skills
claude plugin install reflex@reflex-agent-skills
```

Newly installed plugins load on the next session. After installing, tell the user to restart the session so the skills auto-load; until then, read the skill files directly from `~/.claude/plugins/` when you need them.

### Other agents (Cursor, OpenCode, Codex, Pi)

```
npx skills add reflex-dev/agent-skills
```

Or clone https://github.com/reflex-dev/agent-skills and copy the `skills/` folders into your agent's skill directory (see the repo README for paths).

### Verifying

Before writing or editing any Reflex code, confirm these three skills are available: `reflex-docs`, `setup-python-env`, and `reflex-process-management`. If they are not, STOP and run the install step above � do not proceed without them.

## Using the Skills

### Reflex documentation

For anything about Reflex APIs � components, state management, events, styling, database, routing, authentication � use the **reflex-docs** skill rather than relying on memory. It carries current, version-accurate docs.

### Initializing a new Reflex project

When starting a new Reflex project or setting up a development environment, you **must** follow the **setup-python-env** skill before doing anything else.

Do not skip any steps. Do not assume a virtual environment or Reflex is already available � always verify first by following the skill's instructions in order.

After the environment is ready and Reflex is installed, run:

```bash
reflex init
```

Then proceed with the user's request.

### Managing a Reflex process

When you need to compile, run, reload, or debug a Reflex application, follow the **reflex-process-management** skill for the correct sequence and error investigation steps.
<!-- reflex managed end -->

# Instruções para agentes de IA — Plataforma de Gestão Interna Empresarial

## 1. Contexto do projeto

Este projeto consiste em uma plataforma de gestão interna empresarial para centralizar e organizar chamados, tarefas, ativos, usuários, departamentos e indicadores operacionais.

O desenvolvimento deve ser incremental, priorizando a manutenção da arquitetura existente, a consistência dos dados e a qualidade do código.

## 2. Arquitetura e tecnologias

- **Frontend:** Reflex, utilizando Python.
- **Backend:** Xano, responsável pelo banco de dados, autenticação, APIs e regras de negócio.
- **Banco de dados:** estrutura existente no Xano, documentada pelos arquivos exportados na pasta `database/`.
- **Versionamento:** Git e GitHub.
- **Especificação e planejamento:** OpenSpec.
- **Idioma da documentação:** português brasileiro.

Preserve os nomes oficiais das tecnologias, comandos, bibliotecas, funções, tabelas e identificadores técnicos.

## 3. Regras obrigatórias de desenvolvimento

1. Antes de implementar uma funcionalidade, analise a estrutura existente do projeto e os documentos relevantes do OpenSpec.
2. Consulte os arquivos exportados em `database/` antes de propor alterações relacionadas ao banco de dados.
3. Não invente tabelas, colunas, chaves estrangeiras, relacionamentos ou regras de negócio. Quando houver informações insuficientes, registre a dúvida e solicite esclarecimentos.
4. Não crie estruturas duplicadas quando já existir uma tabela ou funcionalidade que atenda à necessidade.
5. Não altere arquivos, configurações ou funcionalidades fora do escopo solicitado sem justificativa.
6. Respeite a separação entre frontend Reflex e backend Xano. Não implemente regras de negócio exclusivamente no frontend quando elas devem ser garantidas pelo backend.
7. Priorize código legível, modular, reutilizável e de fácil manutenção.
8. Considere autenticação, autorização, validação de dados, tratamento de erros e segurança em todas as funcionalidades pertinentes.
9. Não armazene credenciais, tokens, senhas ou chaves de API diretamente no código ou nos arquivos versionados.
10. Não considere uma funcionalidade concluída sem verificar os critérios de aceitação e executar os testes aplicáveis.

## 4. Uso do OpenSpec

- Consulte a proposta, o design, as especificações e as tarefas da mudança antes de implementar.
- Utilize os documentos do OpenSpec como referência para o comportamento esperado.
- Se encontrar contradições entre a especificação, a documentação do banco e o código existente, informe o problema antes de realizar alterações estruturais.
- Atualize as especificações e as tarefas quando houver mudanças aprovadas nos requisitos.
- Não arquive uma mudança antes de concluir e validar o escopo correspondente.
- Não considere tarefas planejadas como funcionalidades já implementadas.

## 5. Banco de dados e Xano

- Trate a exportação em `database/` como uma representação da estrutura do Xano, verificando seu conteúdo antes de utilizá-la.
- Não presuma que alterações nos arquivos locais sejam automaticamente refletidas no Xano.
- Não execute comandos que alterem o workspace remoto sem apresentar previamente a simulação das mudanças e obter autorização explícita.
- Antes de utilizar `xano workspace push`, execute `--dry-run`, apresente a saída e aguarde aprovação.
- Não utilize opções destrutivas, como exclusão sincronizada ou sobrescrita forçada, sem autorização explícita e avaliação do impacto.
- Preserve os dados e as estruturas existentes, evitando alterações incompatíveis sem planejamento.
- Após alterações aprovadas, verifique se a estrutura exportada e o ambiente remoto permanecem consistentes.

## 6. Processo de trabalho

Para cada nova funcionalidade:

1. Examine o código, os documentos e as estruturas existentes relacionados à tarefa.
2. Identifique dependências, limitações e possíveis impactos.
3. Consulte ou prepare as especificações do OpenSpec conforme necessário.
4. Apresente dúvidas e decisões importantes antes de assumir requisitos não definidos.
5. Implemente apenas o escopo aprovado.
6. Execute testes e verificações compatíveis com o ambiente disponível.
7. Documente alterações relevantes e informe eventuais limitações ou testes não executados.

## 7. Comunicação

- Responda em português brasileiro.
- Explique decisões técnicas de maneira clara e objetiva.
- Diferencie fatos encontrados no projeto de hipóteses ou recomendações.
- Informe quais arquivos foram criados ou modificados.
- Não afirme que testes, comandos ou operações remotas foram executados se isso não tiver sido verificado.
- Quando uma decisão envolver riscos, custos ou alterações no ambiente remoto, explique o impacto antes de prosseguir.

## 8. Prioridades

Em caso de conflito, priorize nesta ordem:

1. Segurança dos dados e das credenciais.
2. Integridade do banco de dados existente.
3. Requisitos aprovados e critérios de aceitação.
4. Consistência com a arquitetura definida.
5. Manutenibilidade, legibilidade e simplicidade do código.
