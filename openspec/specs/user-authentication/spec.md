# user-authentication Specification

## Purpose
Esta capacidade permite que usuários iniciem e encerrem sessões no frontend, mantendo o contexto seguro do perfil necessário às telas da plataforma e às futuras chamadas autenticadas às APIs.

## Requirements

### Requirement: autenticação com credenciais existentes
O sistema MUST permitir que um usuário autenticado no Xano entre no frontend com seu e-mail e senha, usando o endpoint de login existente e sem expor a senha ou o token em mensagens, registros ou conteúdo apresentado na interface.

#### Scenario: login bem-sucedido
- **WHEN** o usuário informa credenciais válidas
- **THEN** o frontend autentica com o Xano, mantém a sessão e apresenta uma página inicial autenticada
- **AND** disponibiliza para o contexto do usuário somente os dados seguros retornados pela API, incluindo identificador, nome, e-mail, `perfil_id` e `departamento_id`

#### Scenario: credenciais rejeitadas
- **WHEN** o usuário informa credenciais inválidas ou a API rejeita a autenticação
- **THEN** o frontend permanece na tela de login, informa que não foi possível autenticar e não cria uma sessão

#### Scenario: falha de comunicação com o serviço
- **WHEN** não é possível alcançar o endpoint de autenticação
- **THEN** o frontend informa que houve uma falha de comunicação, não apresenta a operação como bem-sucedida e permite nova tentativa

### Requirement: persistência e validação da sessão
O sistema MUST manter o token de autenticação e o perfil seguro no navegador entre reinicializações do navegador, até logout ou expiração do token, e MUST validar a sessão com o Xano antes de permitir acesso ao conteúdo autenticado.

#### Scenario: restauração de sessão válida
- **WHEN** o usuário reabre a aplicação com token armazenado e ainda válido
- **THEN** o frontend valida o token com o Xano, restaura o perfil seguro e apresenta o conteúdo autenticado

#### Scenario: sessão ausente ou expirada
- **WHEN** não há token armazenado ou o Xano rejeita o token durante a validação
- **THEN** o frontend não permite acesso ao conteúdo autenticado, remove o token e o perfil locais quando inválidos e apresenta a tela de login

#### Scenario: armazenamento de perfil para uso posterior
- **WHEN** o Xano retorna o perfil seguro do usuário
- **THEN** o frontend disponibiliza `perfil_id` e `departamento_id` no contexto da sessão para personalização futura da interface
- **AND** as permissões sobre dados e ações continuam sendo verificadas no backend, sem depender apenas do perfil guardado no navegador

### Requirement: páginas e chamadas autenticadas
O sistema MUST restringir páginas autenticadas a sessões validadas e enviar o token armazenado no cabeçalho de autorização das chamadas futuras a endpoints Xano que exigem autenticação.

#### Scenario: acesso sem sessão
- **WHEN** um usuário sem sessão válida tenta abrir diretamente uma página autenticada
- **THEN** o frontend direciona o usuário à tela de login sem expor o conteúdo protegido

#### Scenario: chamada autenticada à API
- **WHEN** o frontend chama um endpoint Xano protegido durante uma sessão válida
- **THEN** a requisição inclui o token de autenticação no cabeçalho esperado pelo Xano

### Requirement: logout local
O sistema MUST oferecer ao usuário autenticado uma ação de logout que encerra a sessão local e remove do navegador o token e os dados de perfil persistidos.

#### Scenario: logout
- **WHEN** o usuário seleciona logout
- **THEN** o frontend remove token e perfil armazenados, encerra o contexto autenticado e apresenta a tela de login
- **AND** não afirma que o token foi revogado no Xano, pois ele pode continuar válido até sua expiração de 24 horas
