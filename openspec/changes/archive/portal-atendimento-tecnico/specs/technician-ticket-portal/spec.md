# Spec Delta

## Purpose

Disponibilizar ao técnico uma área autenticada para consultar todos os chamados e executar o atendimento daqueles aos quais está associado, com identificação do solicitante e histórico de comentários.

## ADDED Requirements

### Requirement: acesso à área técnica
O sistema MUST apresentar a área técnica ao usuário autenticado com `perfil_id` 3 após login ou restauração válida da sessão, mantendo as áreas e permissões dos demais perfis.

#### Scenario: técnico entra na aplicação
- **WHEN** a sessão de um técnico é validada
- **THEN** a aplicação apresenta a lista de chamados e acesso aos detalhes de atendimento

#### Scenario: acesso sem permissão
- **WHEN** uma pessoa sem sessão válida ou com perfil diferente de técnico tenta executar ações técnicas
- **THEN** o backend rejeita a operação e a interface não oferece controles técnicos autorizados indevidamente

### Requirement: consulta global dos chamados
O sistema MUST permitir ao técnico consultar todos os chamados existentes, independentemente de departamento, solicitante, associação e status, tanto na lista quanto por identificador. A ampliação MUST preservar as restrições dos demais perfis e não conceder escrita global.

#### Scenario: chamado de outro técnico ou finalizado
- **WHEN** um técnico consulta um chamado atribuído a outro técnico, resolvido ou fechado
- **THEN** o chamado aparece na lista e seu detalhe e histórico podem ser consultados

#### Scenario: consulta vazia ou inexistente
- **WHEN** não existem chamados ou o identificador consultado não existe
- **THEN** a interface distingue lista vazia de chamado não encontrado sem apresentar dados anteriores

#### Scenario: funcionário consulta chamado alheio
- **WHEN** um funcionário tenta consultar um chamado de outra pessoa
- **THEN** o backend continua negando o acesso

### Requirement: detalhe com contexto e histórico
O sistema MUST exibir número, título, descrição, status, categoria, prioridade, nome e identificação do solicitante, técnicos associados e solução quando disponíveis. O histórico MUST apresentar comentários do chamado selecionado em ordem cronológica com autor e data/hora, sem expor credenciais ou campos privados de usuários.

#### Scenario: técnico abre um detalhe
- **WHEN** o técnico seleciona um chamado
- **THEN** a interface apresenta seu contexto e os comentários vinculados apenas a ele, identificando quem abriu o chamado

#### Scenario: histórico vazio ou indisponível
- **WHEN** não há comentários ou a consulta do histórico falha
- **THEN** a interface distingue ausência de comentários de falha e permite tentar novamente quando houver erro

### Requirement: autoassociação autenticada
O sistema MUST permitir ao técnico associar seu próprio usuário a um chamado em `Aberto`, obtendo sua identidade da sessão no backend e preservando os técnicos já associados. A repetição MUST evitar associações duplicadas; chamados fora de `Aberto` MUST rejeitar novas associações conforme a regra existente.

#### Scenario: técnico assume chamado aberto
- **WHEN** o técnico aciona a autoassociação em um chamado aberto
- **THEN** seu usuário é associado ao chamado e a interface atualiza a lista de técnicos sem remover associações anteriores

#### Scenario: associação repetida ou identidade adulterada
- **WHEN** a operação é repetida ou o cliente tenta indicar outro técnico
- **THEN** não é criado vínculo duplicado nem associação em nome de outra pessoa

#### Scenario: chamado deixa de estar aberto
- **WHEN** um técnico tenta associar-se a um chamado que já não está aberto
- **THEN** o backend rejeita a associação e a interface informa a situação atual

### Requirement: comentários com autoria segura
O sistema MUST permitir ao técnico associado enviar comentário não vazio e consultar o histórico atualizado, vinculando chamado e autor de forma validada no backend. A leitura global MUST NOT permitir comentários por técnico não associado. A permissão de comentar após conclusão para técnico associado permanece conforme o contrato existente.

#### Scenario: comentário válido
- **WHEN** o técnico associado envia um comentário não vazio
- **THEN** o comentário é persistido com a identidade autenticada e apresentado no histórico do chamado

#### Scenario: comentário inválido ou não autorizado
- **WHEN** o comentário está vazio ou o técnico não está associado
- **THEN** o backend rejeita a gravação, inclusive em requisição direta

### Requirement: atualização operacional e conclusão
O sistema MUST permitir ao técnico associado alterar o status para `Em Análise`, `Em atendimento`, `Aguardando usuário`, `Resolvido` ou `Fechado`, conforme a configuração válida do backend. Resolver ou fechar MUST exigir solução final não vazia na mesma operação e registrar a data de resolução. Chamados já resolvidos ou fechados MUST impedir novas alterações operacionais, sem adicionar reabertura.

#### Scenario: iniciar atendimento
- **WHEN** um técnico associado altera um chamado aberto para `Em atendimento`
- **THEN** o backend persiste a mudança e a lista e o detalhe passam a apresentar o status confirmado

#### Scenario: finalizar com solução
- **WHEN** o técnico associado seleciona `Resolvido` ou `Fechado` e informa solução final válida
- **THEN** o sistema persiste status, solução e data de resolução e bloqueia novas alterações operacionais

#### Scenario: tentativa de finalizar sem solução ou sem associação
- **WHEN** falta solução final ou o técnico não está associado ao chamado
- **THEN** o backend rejeita a alteração sem apresentar sucesso ou modificar o chamado

#### Scenario: configuração de status ausente
- **WHEN** o status solicitado não está configurado no backend
- **THEN** a operação é rejeitada com mensagem clara sem presumir identificadores nem criar status

### Requirement: falhas e ciclo da sessão
O sistema MUST informar falhas de consulta e gravação sem simular sucesso, preservar o texto editado quando possível e bloquear envios simultâneos na interface. Dados de atendimento MUST ser limpos ao sair ou invalidar a sessão; troca de chamado MUST evitar mostrar dados e rascunhos do chamado anterior.

#### Scenario: falha ao salvar comentário ou solução
- **WHEN** a API rejeita uma gravação ou a comunicação falha
- **THEN** a interface informa a falha, mantém o texto quando possível e permite nova tentativa sem afirmar que a operação foi concluída

#### Scenario: sessão encerrada
- **WHEN** o usuário sai ou a sessão é rejeitada
- **THEN** a aplicação remove os dados técnicos carregados e exige autenticação para continuar
