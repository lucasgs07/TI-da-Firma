# Spec Delta

## Purpose

Oferecer aos gestores uma área autenticada para consultar e abrir chamados, cadastrar usuários e criar tarefas de acordo com as permissões específicas do departamento de T.I. e dos demais departamentos.

## ADDED Requirements

### Requirement: área gerencial por departamento
O sistema MUST apresentar ao gestor autenticado uma área com recursos correspondentes ao seu departamento validado pelo backend. Alterar dados do navegador MUST NOT conceder permissões adicionais.

#### Scenario: gerente de T.I. acessa a aplicação
- **WHEN** uma sessão de gestor de T.I. é validada
- **THEN** são disponibilizadas consulta global e abertura de chamados, cadastro de usuários e criação de tarefas

#### Scenario: gerente de outro departamento acessa a aplicação
- **WHEN** uma sessão de gestor de outro departamento é validada
- **THEN** são disponibilizados consulta departamental e abertura de chamados e cadastro de funcionários do próprio departamento
- **AND** é disponibilizada criação de tarefas para funcionários do próprio departamento

### Requirement: consulta de chamados sem atendimento gerencial
O sistema MUST permitir ao gestor de T.I. consultar todos os chamados, inclusive concluídos; aos demais gestores, MUST permitir somente chamados cujo solicitante pertença atualmente ao mesmo departamento. “Membro” MUST incluir qualquer perfil desse departamento. Lista, detalhe e histórico MUST respeitar o mesmo escopo no backend. O portal gerencial MUST NOT oferecer atribuição, comentário ou alteração operacional de chamados.

#### Scenario: gestor de T.I. consulta chamado externo
- **WHEN** o gestor de T.I. abre chamado de outro departamento ou finalizado
- **THEN** visualiza seus dados, solicitante e histórico em modo de consulta

#### Scenario: gestor consulta membro do próprio departamento
- **WHEN** um gestor não T.I. consulta chamado de funcionário ou gestor de seu departamento
- **THEN** o chamado pode ser consultado na lista e individualmente, com seu histórico

#### Scenario: tentativa de consultar outro departamento
- **WHEN** o gestor não T.I. informa diretamente o ID de chamado ou interação de solicitante externo ao departamento
- **THEN** o backend nega a leitura sem expor os dados, mesmo que o chamado tenha sido aberto pelo gestor antes de mudar de departamento

### Requirement: abertura de chamado por qualquer gestor
O sistema MUST permitir a qualquer gestor abrir chamado com título, descrição, categoria e prioridade existentes. Solicitante e status inicial MUST ser determinados pelo backend, sem aceitar identidade fornecida pelo navegador.

#### Scenario: gestor registra chamado
- **WHEN** um gestor de T.I. ou de outro departamento envia os dados válidos
- **THEN** o chamado é salvo como solicitação do próprio gestor em status inicial válido e sua criação é confirmada

#### Scenario: envio inválido
- **WHEN** faltam campos obrigatórios ou categoria/prioridade não existe
- **THEN** o backend rejeita a criação e a interface informa os campos ou configuração a corrigir

### Requirement: cadastro global pelo gerente de T.I.
O sistema MUST permitir ao gestor de T.I. criar funcionários e gestores em qualquer departamento existente e técnicos exclusivamente em T.I. O gestor MUST NOT criar administradores. Nome, e-mail único, senha válida, perfil e departamento MUST ser validados no backend; respostas e logs MUST NOT conter senha ou token.

#### Scenario: cadastro de funcionário ou gestor
- **WHEN** o gestor de T.I. escolhe funcionário ou gestor e um departamento existente
- **THEN** o novo usuário é associado exatamente ao perfil e departamento selecionados

#### Scenario: cadastro de técnico
- **WHEN** um novo técnico é cadastrado por um ator autorizado
- **THEN** é associado obrigatoriamente a T.I., inclusive quando criado por administrador
- **AND** uma tentativa explícita de vinculá-lo a outro departamento é rejeitada

#### Scenario: tentativa de criar administrador
- **WHEN** o gestor de T.I. envia cadastro com perfil administrador por requisição direta
- **THEN** o backend rejeita a criação

#### Scenario: dados inválidos ou e-mail duplicado
- **WHEN** o cadastro contém e-mail existente, senha inválida, perfil inválido ou departamento inexistente
- **THEN** o cadastro é rejeitado sem criar usuário parcial nem revelar segredos

### Requirement: cadastro restrito pelos demais gestores
O sistema MUST permitir ao gestor não T.I. cadastrar exclusivamente funcionários no próprio departamento, obtendo o departamento autorizado da sessão. MUST negar perfis técnico, gestor ou administrador e departamentos diferentes, inclusive por requisição direta.

#### Scenario: cadastro departamental válido
- **WHEN** o gestor não T.I. cadastra funcionário com dados válidos
- **THEN** o novo usuário recebe perfil funcionário e o departamento autenticado do gestor

#### Scenario: adulteração de perfil ou departamento
- **WHEN** o gestor não T.I. tenta cadastrar técnico, gestor, administrador ou funcionário de outro departamento
- **THEN** o backend rejeita a criação e não grava o usuário

### Requirement: criação e atribuição de tarefas por departamento
O sistema MUST permitir ao gestor de T.I. criar tarefas somente para técnicos de T.I. e aos demais gestores criar tarefas somente para funcionários do próprio departamento. A tarefa MUST conter título, prioridade existente e responsável elegível, com descrição, prazo e vínculo a chamado opcionais conforme os campos existentes e a visibilidade do chamado. Solicitante e status inicial MUST ser definidos pelo servidor. As opções de responsáveis MUST permitir acesso aos usuários elegíveis sem omitir páginas do diretório.

#### Scenario: tarefa atribuída a técnico elegível
- **WHEN** o gestor de T.I. envia tarefa válida para técnico de T.I.
- **THEN** a tarefa é persistida com o responsável escolhido e o gestor autenticado como solicitante

#### Scenario: responsável inválido ou alterado durante o cadastro
- **WHEN** o responsável não existe ou seu perfil/departamento não corresponde à regra do gestor no momento da gravação
- **THEN** o backend rejeita a atribuição, inclusive tentativas de contornar a regra por atualização

#### Scenario: gestor de outro departamento cria tarefa
- **WHEN** um gestor não T.I. cria tarefa para funcionário do próprio departamento
- **THEN** o backend persiste a tarefa com esse funcionário como responsável e o gestor como solicitante

#### Scenario: atribuição fora do escopo
- **WHEN** um gestor não T.I. atribui tarefa a técnico, gestor ou funcionário de outro departamento, ou um gestor T.I. atribui tarefa a funcionário
- **THEN** o backend rejeita a atribuição sem criar ou reatribuir a tarefa

#### Scenario: diretório contém mais de uma página
- **WHEN** há responsáveis elegíveis além da primeira página
- **THEN** eles continuam acessíveis pelo seletor sem exibir usuários inelegíveis ou dados privados

### Requirement: tarefas próprias do funcionário e solução obrigatória
O sistema MUST permitir ao funcionário listar e consultar exclusivamente as tarefas em que ele é o responsável e concluí-las informando uma solução não vazia. O backend MUST validar a identidade autenticada, registrar solução, status de conclusão e data gerada no servidor, sem permitir que o funcionário altere responsável, solicitante ou outros campos imutáveis. Concluir tarefa vinculada a chamado MUST NOT resolver ou modificar o chamado. O acesso a chamados permanece sujeito às permissões existentes, independentemente da tarefa.

#### Scenario: técnico ou funcionário acessa a tela separada de tarefas
- **WHEN** um técnico ou funcionário seleciona Minhas tarefas na navegação
- **THEN** acessa uma tela própria de tarefas, separada da tela de chamados, contendo somente tarefas atribuídas a ele
- **AND** pode abrir o detalhe e concluir tarefa própria com solução obrigatória conforme as regras já autorizadas ao seu perfil

#### Scenario: navegação entre módulos
- **WHEN** o técnico ou funcionário alterna entre Chamados e Minhas tarefas
- **THEN** o conteúdo de tarefas não é exibido junto da lista ou do detalhe de chamados
- **AND** as permissões existentes de atendimento de chamados não são ampliadas

#### Scenario: funcionário conclui tarefa própria
- **WHEN** o funcionário responsável envia uma solução válida para sua tarefa
- **THEN** a tarefa é concluída com solução e data persistidas e continua consultável após recarga
- **AND** nenhum chamado é resolvido pela operação

#### Scenario: tarefa alheia ou solução ausente
- **WHEN** o funcionário tenta consultar/concluir tarefa alheia ou concluir tarefa própria sem solução válida
- **THEN** o backend rejeita a operação sem alterar a tarefa

#### Scenario: tentativa de resolver chamado
- **WHEN** o funcionário tenta usar a conclusão de tarefa ou uma requisição direta para resolver um chamado
- **THEN** o backend mantém a restrição de atendimento do chamado, inclusive quando estiver vinculado à tarefa

#### Scenario: tarefa concluída e repetição
- **WHEN** o funcionário repete a conclusão da própria tarefa já concluída
- **THEN** uma solução idêntica preserva o registro e a data originais, enquanto uma solução diferente é rejeitada

### Requirement: múltiplos responsáveis e conclusão global da tarefa
O sistema MUST permitir selecionar um ou mais responsáveis na criação de uma tarefa, validando todos antes de gravar. Gestor T.I. MUST selecionar somente técnicos de T.I.; demais gestores MUST selecionar somente funcionários do próprio departamento. A tarefa MUST aparecer uma única vez para cada associado, inclusive os que não são o primeiro da lista. Qualquer associado MUST poder concluir a tarefa inteira com solução obrigatória, e todos MUST consultar o mesmo status, data e solução. A operação MUST NOT modificar chamados.

#### Scenario: vários responsáveis elegíveis
- **WHEN** o gestor seleciona vários usuários elegíveis e envia uma tarefa válida
- **THEN** todos são associados à mesma tarefa e podem consultá-la em Minhas tarefas
- **AND** identificadores repetidos não criam associações duplicadas

#### Scenario: seleção parcialmente inválida
- **WHEN** algum selecionado não existe ou está fora do perfil/departamento permitido
- **THEN** o backend rejeita o envio inteiro sem criar ou reatribuir parcialmente a tarefa

#### Scenario: segundo responsável conclui
- **WHEN** um associado que não é o primeiro responsável informa uma solução válida e conclui a tarefa
- **THEN** a tarefa inteira fica concluída para todos os responsáveis, com a mesma solução e data

#### Scenario: compatibilidade com tarefa antiga
- **WHEN** uma tarefa anterior não tem a lista de responsáveis preenchida
- **THEN** seu responsável único continua autorizado a consultar e concluir a tarefa
- **AND** uma lista nova preenchida prevalece sobre o campo legado para decidir a autorização

#### Scenario: reatribuição de conjunto fora do escopo
- **WHEN** um gestor tenta reatribuir uma tarefa cujo conjunto atual ou novo de responsáveis não está integralmente no seu escopo
- **THEN** o backend rejeita a alteração, sem usar apenas o primeiro responsável como autorização

### Requirement: segurança e feedback dos formulários gerenciais
O sistema MUST distinguir consultas vazias de falhas, bloquear envios simultâneos e confirmar gravações apenas após sucesso do backend. MUST preservar dados não secretos em falhas quando possível, sem persistir senhas em armazenamento do navegador ou logs. Logout e rejeição da sessão MUST limpar dados gerenciais; os portais e autorizações de outros perfis MUST ser preservados, salvo a regra explicitamente definida para novos técnicos.

#### Scenario: API nega operação com sessão válida
- **WHEN** a API rejeita dados ou autorização de uma operação
- **THEN** a interface informa o erro sem afirmar sucesso ou encerrar indevidamente a sessão

#### Scenario: sessão expirada ou logout
- **WHEN** a sessão é rejeitada ou o usuário sai
- **THEN** os dados gerenciais e senhas do formulário são limpos e o conteúdo exige nova autenticação

#### Scenario: regressão de outros perfis
- **WHEN** funcionário, técnico ou administrador usa suas operações existentes
- **THEN** suas permissões permanecem válidas, exceto que novos técnicos devem obrigatoriamente pertencer a T.I.
