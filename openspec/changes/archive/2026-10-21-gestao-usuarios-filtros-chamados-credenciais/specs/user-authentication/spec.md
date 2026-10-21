# Spec Delta

## ADDED Requirements

### Requirement: aplicação do status e permissões atuais da conta
O sistema MUST rejeitar login de conta Inativa e negar chamadas protegidas com tokens emitidos antes da inativação. MUST obter perfil e departamento atuais do backend em cada operação protegida, sem depender de dados persistidos no navegador ou de permissões antigas do token. Contas legadas com status ausente MUST preservar compatibilidade até normalização revisada; status Inativo explícito MUST sempre bloquear acesso. Rejeição da sessão MUST limpar os dados locais conforme os requisitos existentes.

#### Scenario: conta inativada antes do login
- **WHEN** uma conta Inativa informa credenciais corretas
- **THEN** o backend não emite sessão operacional e o frontend não concede acesso

#### Scenario: conta inativada durante uma sessão
- **WHEN** uma conta com token ainda não expirado é inativada
- **THEN** sua próxima consulta ou mutação protegida é negada, sem depender da expiração do token
- **AND** a interface limpa a sessão ao receber sua rejeição

#### Scenario: mudança de perfil ou departamento
- **WHEN** o administrador altera o perfil ou departamento de usuário com sessão aberta
- **THEN** a próxima operação aplica as permissões atuais sem usar o escopo anterior

#### Scenario: compatibilidade de conta antiga
- **WHEN** uma conta antiga não possui status preenchido
- **THEN** o acesso válido existente é preservado até uma normalização explicitamente revisada
