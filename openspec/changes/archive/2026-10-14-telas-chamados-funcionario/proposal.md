# Proposal

## Why

O login já disponibiliza o perfil do usuário, mas a aplicação ainda apresenta apenas uma página inicial genérica e não oferece ao funcionário um fluxo para registrar e acompanhar suas solicitações. Esta mudança habilita o autoatendimento para o perfil Funcionário (`perfil_id` 4), mantendo a visibilidade dos chamados limitada ao solicitante autenticado.

## What Changes

- Criar a experiência do funcionário para consultar seus próprios chamados e iniciar a abertura de um chamado.
- Permitir abrir chamado com título, descrição, categoria e prioridade, usando as APIs autenticadas existentes e o usuário autenticado como solicitante.
- Carregar categorias e prioridades pelas APIs de consulta existentes; usar as categorias informadas para garantir que o conjunto esperado esteja configurado no Xano.
- Exibir detalhes do chamado selecionado sem permitir que o funcionário leia chamados de outras pessoas.
- Reforçar o escopo de leitura no backend e tratar erros e sessões inválidas sem apresentar falhas como operações concluídas.

## Capabilities

### New Capabilities

- `employee-ticket-portal`: experiência do funcionário para abrir chamados e acompanhar apenas os chamados que ele próprio solicitou.

### Modified Capabilities

- Nenhuma capacidade existente no diretório de especificações principais precisa ter seus requisitos alterados; a autenticação já fornece o perfil seguro e exige autorização reforçada no backend.

## Impact

- Frontend Reflex: ampliar a página autenticada e o estado da aplicação para navegação de chamados do funcionário, formulário de abertura, listagem e visualização de detalhes.
- Cliente Xano: adicionar chamadas autenticadas para listar/criar/consultar chamados e carregar categorias e prioridades, conforme contratos exportados.
- Xano: verificar a existência dos registros de categoria `Hardware`, `Software`, `Rede`, `Acesso`, `Impressora` e `Outros`; preservar registros existentes e não alterar o workspace remoto sem autorização e simulação prévias.
- Testes: cobrir o fluxo de funcionário, integração HTTP simulada, falhas de API e isolamento dos dados entre solicitantes.
