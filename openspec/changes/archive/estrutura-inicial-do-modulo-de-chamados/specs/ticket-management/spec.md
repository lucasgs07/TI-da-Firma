# Delta de especificação

## Propósito

A capacidade de gestão de chamados permite registrar, acompanhar e resolver solicitações internas com visão clara de responsabilidade, histórico e indicadores básicos de operação. Ela cobre o fluxo mínimo do MVP e garante que o atendimento seja rastreável por usuário, departamento, ativo e tarefa.

## ADDED Requirements

### Requirement: registro do chamado e contexto inicial (MUST)
O sistema deve permitir que um usuário com perfil adequado registre um chamado com os dados mínimos necessários para descrever a solicitação, o contexto e a origem do pedido.

#### Scenario: criação de chamado por funcionário
- **QUANDO** um funcionário abre um chamado com descrição do problema e dados essenciais do contexto
- **ENTÃO** o sistema deve persistir o chamado, registrar o solicitante e manter o status inicial em um estado válido para o fluxo de atendimento
- **E** o sistema deve permitir que o chamado seja consultado posteriormente pelo solicitante e pelo responsável autorizado

### Requirement: sugestões de categoria e prioridade com apoio de IA (MUST)
O sistema deve oferecer suporte de IA para sugerir categoria e prioridade com base no texto e no contexto do chamado, sem substituir a decisão final do responsável humano.

#### Scenario: recomendação assistida
- **QUANDO** um chamado é criado ou revisado
- **ENTÃO** a plataforma deve apresentar sugestões de categoria e prioridade quando a funcionalidade de IA estiver disponível
- **E** o usuário responsável deve poder aceitar, ajustar ou ignorar a sugestão sem bloquear o fluxo principal

### Requirement: atribuição e atualização durante o atendimento (MUST)
O sistema deve permitir que um técnico ou responsável atribua e atualize um chamado conforme o andamento do atendimento, mantendo o histórico do processo.

#### Scenario: atribuição e atualização por técnico
- **QUANDO** um técnico assume responsabilidade por um chamado
- **ENTÃO** o sistema deve registrar o responsável, permitir a atualização do status e manter o registro das ações realizadas
- **E** o histórico do atendimento deve permitir acompanhar a evolução do chamado de forma verificável

### Requirement: registro de interações e vínculo com ativos (MUST)
O sistema deve permitir registrar as interações do atendimento e associar o chamado a um ativo quando houver relação direta com a solicitação.

#### Scenario: interação e associação a ativo
- **QUANDO** o responsável registra uma interação ou identifica um ativo relacionado ao problema
- **ENTÃO** a plataforma deve manter esse registro no histórico do chamado e refletir a relação com o ativo correspondente
- **E** a associação deve permitir que o chamado e o ativo sejam consultados em conjunto no contexto do atendimento

### Requirement: criação e acompanhamento de tarefas (MUST)
O sistema deve permitir criar tarefas relacionadas ao atendimento e acompanhar sua atribuição e status dentro do fluxo operacional.

#### Scenario: tarefa atribuída ao trabalho do técnico
- **QUANDO** uma tarefa é criada ou atribuída durante o atendimento
- **ENTÃO** o sistema deve registrar o responsável e manter a tarefa visível para acompanhamento no contexto do chamado ou da operação
- **E** o status da tarefa deve contribuir para indicadores básicos de pendência e atraso

### Requirement: controle de acesso por perfil (MUST)
O sistema deve respeitar diferentes perfis de acesso e garantir que somente usuários autorizados possam criar, visualizar, atualizar ou gerenciar chamados conforme o papel de cada usuário.

#### Scenario: acesso por perfil
- **QUANDO** um funcionário, técnico, gestor ou administrador acessa o módulo de chamados
- **ENTÃO** o sistema deve permitir apenas as ações e visualizações compatíveis com as permissões do perfil
- **E** o sistema deve bloquear acessos indevidos mesmo quando o usuário tenha conhecimento do identificador de outro registro

### Requirement: indicadores básicos do módulo (MUST)
O sistema deve disponibilizar indicadores mínimos para acompanhamento executivo do módulo de chamados, com foco no escopo do MVP.

#### Scenario: painel gerencial do módulo
- **QUANDO** um gestor acessa o painel de chamados
- **ENTÃO** o sistema deve apresentar métricas essenciais como quantidade de chamados por status, categoria e prioridade
- **E** o painel deve permitir identificar tarefas pendentes e atrasadas, além de indicar a atividade recente relevante do atendimento

### Requirement: escopo do MVP e evoluções futuras (MUST)
O módulo de chamados deve cobrir o comportamento mínimo necessário para o MVP e separar claramente melhorias futuras do escopo atual.

#### Scenario: evolução controlada do módulo
- **QUANDO** a equipe identificar requisitos futuros como anexos, SLA, auditoria detalhada ou notificações avançadas
- **ENTÃO** esses itens devem ser tratados como expansões do sistema e não como parte do escopo obrigatório do MVP
- **E** a mudança atual deve permanecer focada em abertura, atendimento, histórico, tarefas e indicadores básicos
