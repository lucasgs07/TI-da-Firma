# Spec Delta

## Purpose

Esta capacidade oferece ao funcionário um canal autenticado para registrar chamados e acompanhar as solicitações que ele próprio abriu, sem expor chamados de outros usuários.

## ADDED Requirements

### Requirement: área de chamados exclusiva do funcionário
O sistema MUST disponibilizar as telas de consulta e abertura de chamados aos usuários autenticados cujo `perfil_id` seja 4. O perfil exibido na interface não substitui as verificações de autorização do backend.

#### Scenario: funcionário acessa a área de chamados
- **WHEN** um usuário autenticado com `perfil_id` 4 acessa a aplicação
- **THEN** o sistema apresenta as opções de consultar seus chamados e abrir um chamado

#### Scenario: outro perfil tenta acessar a área do funcionário
- **WHEN** um usuário autenticado com perfil diferente de 4 tenta acessar diretamente uma tela exclusiva do funcionário
- **THEN** o sistema não apresenta dados nem permite ações dessa área e informa que o acesso não está autorizado

### Requirement: consulta restrita aos chamados próprios
O sistema MUST apresentar ao funcionário somente chamados cujo solicitante seja o usuário autenticado, usando o escopo aplicado pelo backend como fonte de autorização. A mesma restrição MUST valer para a consulta individual de um chamado, inclusive quando o funcionário informa diretamente o identificador de outro registro.

#### Scenario: funcionário consulta seus chamados
- **WHEN** um funcionário abre a lista de chamados
- **THEN** a lista contém somente chamados que ele próprio abriu
- **AND** a lista permite distinguir os chamados pelo título, status, categoria e prioridade retornados pela API

#### Scenario: funcionário consulta chamado de outra pessoa
- **WHEN** um funcionário tenta abrir diretamente o detalhe de um chamado de outro solicitante
- **THEN** o backend nega a consulta e a interface não exibe os dados do chamado

#### Scenario: lista sem chamados próprios
- **WHEN** a API retorna uma lista vazia para o funcionário autenticado
- **THEN** a interface informa que ele ainda não abriu chamados e oferece a ação para abrir um

### Requirement: abertura de chamado pelo funcionário
O sistema MUST permitir que o funcionário registre um chamado informando título, descrição, categoria e prioridade. O solicitante e o status inicial MUST ser definidos pelo backend a partir da sessão e da configuração válida do sistema, não por valores de identidade enviados pela interface.

#### Scenario: envio válido do formulário
- **WHEN** o funcionário envia título, descrição, categoria e prioridade válidos
- **THEN** o backend registra o chamado associado ao usuário autenticado e ao status inicial configurado como aberto
- **AND** a interface confirma a criação e atualiza a lista de chamados próprios

#### Scenario: dados obrigatórios ausentes
- **WHEN** o funcionário tenta enviar o formulário sem título, descrição, categoria ou prioridade válidos
- **THEN** a interface informa os campos que precisam ser corrigidos e não apresenta a operação como concluída

#### Scenario: API rejeita ou não conclui a criação
- **WHEN** o backend rejeita a requisição ou ocorre uma falha de comunicação
- **THEN** a interface informa a falha, mantém os dados preenchidos quando possível e permite nova tentativa sem duplicar uma confirmação de sucesso

### Requirement: categorias e prioridades disponíveis no formulário
O sistema MUST carregar as opções do Xano autenticado e apresentar as categorias e prioridades existentes, sem presumir nomes ou identificadores a partir de valores fixos na interface. Os identificadores retornados pelo Xano MUST ser usados ao enviar o formulário.

#### Scenario: formulário carrega as opções configuradas
- **WHEN** o funcionário inicia a abertura de um chamado
- **THEN** a interface carrega categorias e prioridades disponíveis pelas consultas autenticadas
- **AND** apresenta as opções retornadas pelo Xano, vinculando cada seleção ao identificador correspondente retornado pela API

#### Scenario: configuração contém categorias válidas além da lista inicialmente informada
- **WHEN** a API retorna categorias e prioridades com identificadores válidos, mesmo que a lista seja diferente da configuração inicialmente informada
- **THEN** a interface permite selecionar essas opções e enviar seus identificadores retornados pelo Xano

#### Scenario: configuração de categoria incompleta ou consulta indisponível
- **WHEN** a API não retorna categorias ou prioridades, ou a consulta falha
- **THEN** a interface informa que as opções não puderam ser carregadas corretamente e não permite enviar um chamado com opções inválidas

### Requirement: detalhe do chamado próprio
O sistema MUST permitir que o funcionário abra um chamado da própria lista para consultar seus dados retornados pela API, sem disponibilizar ações de atendimento reservadas a outros perfis.

#### Scenario: funcionário abre o detalhe de chamado próprio
- **WHEN** o funcionário seleciona um chamado que ele próprio abriu
- **THEN** a interface apresenta os dados disponíveis do chamado, incluindo título, descrição, status, categoria e prioridade
- **AND** não oferece ações para atribuir, alterar status ou editar dados de atendimento
