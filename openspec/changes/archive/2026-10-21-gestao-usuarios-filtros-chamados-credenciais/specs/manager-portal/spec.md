# Spec Delta

## ADDED Requirements

### Requirement: preservação do cadastro gerencial com senha manual
O sistema MUST manter o cadastro por gestores com senha inicial definida manualmente e validada no backend pelas regras existentes. MUST preservar integralmente as restrições existentes: gestor T.I. cria gestores/funcionários nos departamentos permitidos e técnicos somente em T.I., nunca administradores; demais gestores criam somente funcionários do próprio departamento. MUST NOT conceder edição administrativa aos gestores, gerar senha ou enviar credenciais iniciais por e-mail.

#### Scenario: cadastro pelo gestor de T.I.
- **WHEN** o gestor de T.I. cadastra usuário elegível com senha manual válida
- **THEN** a conta é criada no perfil e departamento autorizados, sem envio automático de credenciais

#### Scenario: cadastro departamental
- **WHEN** um gestor não T.I. cadastra funcionário com senha manual válida
- **THEN** o departamento é derivado da sessão e o perfil permanece funcionário

#### Scenario: adulteração do cadastro
- **WHEN** o gestor envia senha inválida, perfil não permitido ou departamento fora de seu escopo
- **THEN** o backend rejeita sem criar conta
