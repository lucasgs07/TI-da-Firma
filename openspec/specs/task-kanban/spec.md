# task-kanban Specification

## Purpose

Permite que equipes organizem tarefas em quadros Kanban próprios, com etapas configuráveis, movimentação controlada e filtros compatíveis com o escopo de acesso de cada usuário.

## Requirements

### Requirement: Quadro Kanban configurável por equipe
O sistema MUST permitir configurar etapas ordenadas para quadros associados a uma equipe ou departamento, sem alterar os status de chamados.

#### Scenario: Gestor configura o quadro de sua equipe
- **WHEN** um gestor autorizado cria ou altera etapas do quadro de seu departamento
- **THEN** o sistema persiste a configuração somente para o departamento permitido ao gestor
- **AND** preserva a ordem das etapas configuradas

#### Scenario: Administrador configura quadros
- **WHEN** um administrador autorizado cria ou altera um quadro
- **THEN** o sistema permite configurar o quadro para o departamento selecionado dentro do escopo administrativo

#### Scenario: Usuário sem permissão altera configuração
- **WHEN** um técnico ou funcionário tenta criar, reordenar ou alterar etapas diretamente na API
- **THEN** o backend nega a operação sem modificar o quadro

#### Scenario: Tarefa com responsáveis em vários departamentos
- **WHEN** uma tarefa tem responsáveis em mais de um departamento
- **THEN** o sistema exibe um cartão da tarefa em cada quadro dos departamentos distintos envolvidos
- **AND** mantém uma única associação por tarefa e departamento, mesmo quando há vários responsáveis no mesmo departamento

### Requirement: Visualização de tarefas no quadro
O sistema MUST exibir em cada etapa as tarefas que pertencem ao quadro da equipe e cuja etapa atual corresponda àquela coluna, respeitando o escopo de acesso do usuário.

#### Scenario: Membro consulta tarefas permitidas
- **WHEN** um usuário autorizado consulta um quadro
- **THEN** o sistema retorna somente tarefas e informações que o usuário pode acessar conforme seu perfil, equipe e atribuição
- **AND** não revela tarefas de equipes não autorizadas

#### Scenario: Equipe ainda não possui quadro configurado
- **WHEN** uma equipe não tem etapas configuradas
- **THEN** o sistema informa que o quadro não está configurado
- **AND** não inventa etapas nem apresenta a lista como um quadro configurado

### Requirement: Movimentação de tarefas entre etapas
O sistema MUST permitir que usuários autorizados movam a etapa de uma associação tarefa-quadro sem alterar as etapas da mesma tarefa em outros quadros e MUST validar a transição e o acesso no backend.

#### Scenario: Tarefa movida para etapa válida
- **WHEN** um usuário autorizado solicita mover uma tarefa para uma etapa existente do quadro de sua equipe
- **THEN** o backend atualiza a etapa da tarefa e a resposta confirma o estado persistido
- **AND** o quadro apresenta a tarefa na nova etapa após a confirmação

#### Scenario: Tarefa compartilhada movida em um quadro
- **WHEN** um usuário autorizado move a tarefa em um dos quadros em que ela aparece
- **THEN** o sistema altera somente a etapa da associação com aquele departamento
- **AND** preserva as etapas da mesma tarefa nos demais quadros

#### Scenario: Etapa ou quadro não corresponde à tarefa
- **WHEN** uma solicitação referencia uma etapa inexistente, de outro quadro ou uma tarefa fora do escopo do usuário
- **THEN** o backend rejeita a movimentação sem alterar a tarefa

#### Scenario: Falha ao persistir movimentação
- **WHEN** a movimentação é rejeitada ou não pode ser confirmada pelo backend
- **THEN** a interface mantém ou restaura a tarefa na etapa confirmada anteriormente
- **AND** informa que a operação não foi concluída

#### Scenario: Tarefa concluída globalmente
- **WHEN** um responsável autorizado conclui uma tarefa que aparece em vários quadros
- **THEN** a conclusão e sua data são registradas globalmente pela operação de tarefas existente
- **AND** cada associação da tarefa é movida para a etapa terminal configurada no respectivo quadro

### Requirement: Filtragem de tarefas no Kanban
O sistema MUST permitir filtrar tarefas por responsável, equipe e prioridade, aplicando no backend os limites de acesso independentemente dos filtros escolhidos.

#### Scenario: Filtrar tarefas autorizadas
- **WHEN** um usuário aplica filtros de responsável, equipe ou prioridade
- **THEN** o sistema exibe somente as tarefas que correspondem aos filtros e que o usuário está autorizado a consultar

#### Scenario: Filtro tenta ampliar acesso
- **WHEN** um gestor ou técnico solicita no filtro uma equipe ou tarefa fora de seu escopo
- **THEN** o backend mantém o escopo autorizado ou nega a consulta sem expor os registros solicitados
