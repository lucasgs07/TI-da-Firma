# ticket-search Specification

## Purpose

Oferecer filtros consistentes de chamados aos quatro perfis, permitindo localizar solicitações sem ampliar o escopo de dados ou as ações de atendimento autorizadas pelo backend.

## Requirements

### Requirement: filtros combinados em todos os portais
O sistema MUST oferecer prioridade, status e pesquisa por nome do solicitante nas listas de chamados de administrador, gestor, técnico e funcionário. Prioridade e status MUST usar registros existentes, sem IDs presumidos. A busca de nome MUST ser parcial, ignorar maiúsculas/minúsculas e espaços externos, com limite de 200 caracteres. Filtros diferentes MUST ser combinados por interseção; ausência de filtro MUST preservar a consulta atual. MUST oferecer aplicar e limpar filtros, preservando a busca existente por número/título.

#### Scenario: combinação de filtros
- **WHEN** um usuário aplica prioridade Alta, status Aberto e trecho de nome `MARINA`
- **THEN** os resultados satisfazem os três filtros simultaneamente dentro de seu escopo autorizado

#### Scenario: limpar filtros
- **WHEN** o usuário limpa prioridade, status e solicitante
- **THEN** a lista volta a consultar todos os chamados autorizados, sem ampliar o escopo do perfil

#### Scenario: filtro inválido ou resultado vazio
- **WHEN** o usuário informa um ID inexistente ou nome acima do limite
- **THEN** recebe erro de entrada sem consulta ampliada
- **AND** consulta válida sem correspondências apresenta lista vazia, distinta de falha de comunicação

### Requirement: autorização anterior ao refinamento
O backend MUST aplicar os filtros em conjunto com o escopo derivado da sessão, sem usar o filtro como autorização. Administradores e técnicos preservam leitura global; gestor T.I. preserva leitura global e demais gestores somente seu departamento; funcionários somente chamados próprios. MUST NOT expor diretório global para pesquisar solicitantes. Filtrar MUST NOT conceder ações de atendimento, alterar registros ou ampliar as permissões atuais de escrita dos técnicos.

#### Scenario: funcionário pesquisa outra pessoa
- **WHEN** um funcionário busca o nome de solicitante de outro usuário
- **THEN** nenhum chamado de outra pessoa é retornado

#### Scenario: gestor pesquisa outro departamento
- **WHEN** um gestor não T.I. filtra por solicitante externo ao seu departamento
- **THEN** os chamados externos permanecem inacessíveis, inclusive por requisição direta

#### Scenario: técnico consulta e tenta editar
- **WHEN** um técnico localiza chamado pelo filtro e tenta uma ação de atendimento
- **THEN** continuam obrigatórias as verificações existentes de associação, status e solução final
- **AND** admin, gestor e funcionário não recebem novos controles de atendimento

#### Scenario: chamada sem sessão válida
- **WHEN** um cliente chama a consulta filtrada sem autenticação válida
- **THEN** o backend rejeita sem revelar resultados ou opções provenientes de dados restritos
