# Spec Delta

## Purpose

Permitir ao administrador consultar e editar os usuários existentes, preservando o cadastro autorizado com senha inicial definida manualmente e a proteção dos dados sensíveis.

## ADDED Requirements

### Requirement: listagem administrativa completa
O sistema MUST permitir somente ao administrador listar e consultar todos os usuários cadastrados, ativos e inativos, de qualquer perfil e departamento. MUST apresentar identificador, nome, e-mail, perfil, departamento e status disponíveis, com paginação que alcance todos os registros, sem expor senha, hash ou tokens. O cadastro existente MUST continuar disponível na mesma área.

#### Scenario: diretório com várias páginas
- **WHEN** o administrador navega na área Usuários
- **THEN** consegue alcançar todos os usuários sem truncamento ou duplicação de registros
- **AND** pode cadastrar novo usuário ou abrir um existente

#### Scenario: usuário sem permissão administrativa
- **WHEN** gestor, técnico ou funcionário chama diretamente o detalhe ou a edição administrativos
- **THEN** o backend nega o acesso, preservando somente as consultas gerenciais já autorizadas

### Requirement: edição administrativa validada
O sistema MUST permitir ao administrador editar nome, e-mail, perfil, departamento e status Ativo/Inativo de usuário existente. MUST validar e-mail único, referências e técnico exclusivamente em T.I., rejeitar alteração de senha/ID ou campos fora dessa lista e preservar associações de chamados e tarefas. MUST impedir que edição ou inativação remova o último administrador ativo, inclusive sob concorrência.

#### Scenario: alteração válida e persistente
- **WHEN** o administrador salva dados válidos e recarrega a lista e o detalhe
- **THEN** os novos valores persistem e o sucesso só é mostrado após confirmação do backend
- **AND** chamados, tarefas e histórico existentes não são apagados nem reatribuídos

#### Scenario: dados inválidos
- **WHEN** a edição contém e-mail de outro usuário, referência inválida, técnico fora de T.I. ou campo proibido
- **THEN** o backend rejeita sem alteração parcial e a interface preserva os dados não secretos para correção

#### Scenario: proteção do último administrador
- **WHEN** uma ou mais edições concorrentes deixariam o sistema sem administrador ativo
- **THEN** o backend rejeita as alterações necessárias para manter pelo menos um administrador ativo

### Requirement: cadastro com senha manual preservado
O sistema MUST manter a definição manual da senha inicial pelo administrador ou gestor autorizado, com as validações existentes de mínimo de oito caracteres, uma letra e um número. MUST persistir somente o hash no backend, não retornar senha em respostas nem armazená-la em logs ou armazenamento persistente do navegador. MUST NOT gerar ou enviar automaticamente senha inicial por e-mail, nem exigir sufixo fixo. A edição cadastral MUST NOT redefinir senha.

#### Scenario: cadastro autorizado
- **WHEN** administrador ou gestor fornece dados e senha inicial válidos no seu escopo
- **THEN** o usuário é criado com essa senha e com as restrições existentes de perfil e departamento
- **AND** a criação não depende de envio de e-mail

#### Scenario: senha inválida
- **WHEN** a senha não atende às regras existentes
- **THEN** o backend rejeita sem cadastro parcial e a interface informa a necessidade de correção sem exibir a senha

#### Scenario: edição e migração
- **WHEN** a mudança é publicada ou o admin edita os dados cadastrais de uma conta
- **THEN** a senha existente permanece inalterada e não é enviada por e-mail
