# Proposal

## Why

O administrador ainda recebe uma entrada genérica no frontend, apesar de já possuir permissões globais no Xano. Uma área própria permitirá acompanhar os chamados, consultar tarefas e históricos e cadastrar usuários sem depender de acesso direto ao backend.

## What Changes

- Dashboard com contagens globais de chamados abertos, em andamento e finalizados, sem depender de atribuição a técnicos.
- Consulta de todos os chamados e tarefas, com detalhe, solicitante e responsáveis, preservando múltiplos associados e registros antigos.
- Cadastro de administrador, gestor, técnico e funcionário; departamentos existentes selecionáveis, com técnicos obrigatoriamente em T.I., conforme confirmação do usuário.
- Consulta do histórico dos chamados e download em CSV, individual ou de todos os chamados, com campos públicos e proteção contra fórmulas em planilhas.
- Acesso a chamados e tarefas somente para consulta nesta etapa; o portal não oferece atendimento, atribuição, conclusão ou exclusão.

## Capabilities

### New Capabilities

- `admin-portal`: dashboard global, consultas administrativas, cadastro global de usuários e consulta/exportação do histórico de chamados.

### Modified Capabilities

Nenhuma. Preservar as regras das capacidades existentes, incluindo técnicos novos exclusivamente em T.I.

## Impact

Frontend Reflex: entrada por perfil em `TI_da_Firma.py`, estado e componentes administrativos dedicados, cliente HTTP e limpeza de sessão. Backend Xano: reutilizar leitura de chamados, tarefas, interações e `users/create`; acrescentar métricas globais e consulta/exportação administrativa paginada do histórico conforme contratos do design, mantendo fontes e exportações coerentes.

Não há nova tabela ou coluna prevista. `interacao_chamado` já registra mensagem, chamado, autor e data; `event_log` possui metadados genéricos, mas não comprova auditoria completa por chamado. Neste escopo, logs significam o histórico efetivamente registrado dos chamados, sem inventar eventos passados ou expor metadados genéricos.

Decisões de apresentação propostas: CSV UTF-8 para download; abertos = `Aberto`, em andamento = `Em Análise`, `Em atendimento` e `Aguardando usuário`, finalizados = `Resolvido` e `Fechado`. Status desconhecidos serão contabilizados separadamente como não classificados. Nenhuma mudança remota ocorrerá sem simulação e autorização específica na implementação.
