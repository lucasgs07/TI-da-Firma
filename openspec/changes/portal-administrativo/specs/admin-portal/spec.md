# Spec Delta

## Purpose

Disponibilizar ao administrador uma área global de acompanhamento de chamados e tarefas, cadastro de usuários e consulta e exportação do histórico registrado dos chamados.

## ADDED Requirements

### Requirement: acesso administrativo validado
O sistema MUST disponibilizar o portal administrativo somente a sessões de administrador validadas pelo backend. As consultas administrativas exclusivas e a exportação global MUST validar a identidade e o perfil no servidor, sem confiar no navegador.

#### Scenario: administrador entra ou restaura sessão
- **WHEN** a sessão de administrador é validada
- **THEN** a aplicação apresenta Dashboard, Chamados, Tarefas, Usuários e Logs

#### Scenario: outro perfil tenta obter acesso
- **WHEN** um usuário não administrador altera o perfil local ou chama diretamente uma operação administrativa exclusiva
- **THEN** o acesso é negado sem expor dados administrativos ou ampliar as permissões existentes desse perfil

### Requirement: indicadores globais de chamados
O sistema MUST apresentar contagens globais de chamados abertos, em andamento e finalizados, incluindo chamados sem técnico associado e de qualquer departamento. Abertos MUST corresponder a `Aberto`; em andamento a `Em Análise`, `Em atendimento` e `Aguardando usuário`; finalizados a `Resolvido` e `Fechado`. Cada chamado MUST ser contado uma única vez.

#### Scenario: chamados com vários responsáveis
- **WHEN** existem chamados sem responsável e chamados com vários técnicos
- **THEN** cada registro contribui uma única unidade ao indicador correspondente ao seu status atual

#### Scenario: ausência de dados ou status desconhecido
- **WHEN** não existem chamados ou há chamado com status ausente/desconhecido
- **THEN** o dashboard apresenta zero onde aplicável e contabiliza os desconhecidos separadamente como não classificados
- **AND** uma falha de consulta é apresentada como erro, nunca como contagem zero

### Requirement: consulta global de chamados e tarefas
O sistema MUST permitir ao administrador consultar todos os chamados e tarefas, inclusive finalizados, sem restrição departamental ou de atribuição. Listas e detalhes MUST apresentar campos públicos, solicitante e responsáveis disponíveis, preservando tarefas legadas e múltiplos responsáveis. A navegação MUST permitir alcançar todos os registros sem truncamento silencioso.

#### Scenario: administrador consulta outro departamento
- **WHEN** abre a lista ou o detalhe de chamado ou tarefa de outro departamento
- **THEN** visualiza os dados autorizados, inclusive solução e conclusão quando existentes

#### Scenario: tarefa compartilhada ou legada
- **WHEN** consulta tarefa com vários associados ou somente responsável legado
- **THEN** a tarefa aparece uma única vez e apresenta os responsáveis correspondentes

#### Scenario: consulta sem atendimento
- **WHEN** o administrador navega em chamados ou tarefas neste portal
- **THEN** a interface não oferece criação desses registros, comentários, atribuição, atendimento, conclusão ou exclusão
- **AND** as consultas não provocam mutações nos registros

### Requirement: cadastro administrativo de usuários
O sistema MUST permitir ao administrador criar administradores, gestores, técnicos e funcionários. Departamentos existentes MUST ser selecionáveis para administradores, gestores e funcionários; novos técnicos MUST pertencer exclusivamente a T.I. Nome, e-mail único, senha, perfil e departamento MUST ser validados no backend. Senhas e tokens MUST NOT constar das respostas, downloads ou logs da aplicação.

#### Scenario: cadastro em departamento escolhido
- **WHEN** o administrador cadastra administrador, gestor ou funcionário com dados válidos e departamento existente
- **THEN** o usuário é criado com o perfil e departamento escolhidos, e o sucesso só é exibido após confirmação do servidor

#### Scenario: técnico fora de T.I.
- **WHEN** o administrador seleciona técnico ou envia diretamente outro departamento para esse perfil
- **THEN** o formulário fixa T.I. e o backend rejeita uma tentativa explícita de departamento diferente

#### Scenario: dados inválidos ou envio repetido
- **WHEN** há e-mail duplicado, senha inválida, perfil/departamento inexistente ou envio enquanto outro cadastro está em andamento
- **THEN** a aplicação informa o erro ou bloqueia o segundo envio sem criar cadastro parcial nem expor a senha

### Requirement: consulta do histórico de chamados
O sistema MUST permitir ao administrador consultar o histórico registrado de todos os chamados ou de um chamado selecionado, incluindo data, identificador do chamado, autor e mensagem disponíveis. Os registros MUST ter ordem determinística e navegação completa. O histórico MUST NOT afirmar auditoria de alterações que não foram registradas.

#### Scenario: consulta global e individual
- **WHEN** o administrador abre Logs ou escolhe um chamado
- **THEN** visualiza respectivamente as interações de todos os chamados ou somente as do chamado escolhido, com identificação da origem

#### Scenario: chamado sem histórico ou autor indisponível
- **WHEN** um chamado não possui interações ou seu autor não está mais disponível
- **THEN** a interface indica histórico vazio ou autor indisponível sem inventar eventos nem perder a mensagem existente

### Requirement: download seguro do histórico
O sistema MUST permitir baixar em CSV UTF-8 o histórico completo do escopo selecionado, global ou de um chamado. O arquivo MUST conter apenas identificador da interação, identificador do chamado, data, identificador/nome do autor e mensagem, sem segredos ou metadados genéricos. A exportação MUST tratar aspas, quebras de linha, separadores e textos interpretáveis como fórmulas por planilhas.

#### Scenario: histórico com mais de uma página
- **WHEN** o administrador baixa um histórico que excede uma página
- **THEN** o arquivo inclui todos os registros do escopo, sem duplicações de paginação e sem truncamento silencioso

#### Scenario: conteúdo especial ou histórico vazio
- **WHEN** mensagens contêm acentos, aspas, quebras de linha ou prefixos de fórmula, ou o histórico está vazio
- **THEN** o arquivo preserva a leitura segura dos valores e contém cabeçalho mesmo sem registros

#### Scenario: falha ou sessão rejeitada durante exportação
- **WHEN** a exportação falha ou a autorização deixa de ser válida antes de terminar
- **THEN** nenhum arquivo parcial é apresentado como completo e a interface informa a falha sem disponibilizar dados a outra sessão

### Requirement: isolamento dos dados administrativos
O sistema MUST limpar dados administrativos e conteúdo temporário de downloads em logout, rejeição de sessão ou troca de usuário. MUST distinguir carregamento, vazio, erro e sucesso e preservar as funcionalidades dos demais perfis.

#### Scenario: administrador sai e funcionário entra
- **WHEN** a sessão administrativa termina e outro usuário acessa a aplicação
- **THEN** não há indicadores, listas, histórico, senha ou arquivo administrativo da sessão anterior acessível no estado da nova sessão
