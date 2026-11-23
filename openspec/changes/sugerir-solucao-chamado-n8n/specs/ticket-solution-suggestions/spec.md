# Spec Delta

## Purpose

Permitir que técnicos consultem sugestões de solução geradas por IA no atendimento de um chamado e avaliem o procedimento antes de registrar a solução final.

## ADDED Requirements

### Requirement: Sugestão disponível no atendimento técnico

O sistema MUST disponibilizar **Sugerir solução** junto de **Solução final** exclusivamente a técnicos autorizados a atualizar o atendimento daquele chamado. A autorização MUST ser verificada no servidor antes de acionar o fluxo.

#### Scenario: Técnico associado consulta sugestões

- **WHEN** um técnico autorizado seleciona **Sugerir solução** em um chamado editável
- **THEN** o sistema solicita sugestões ao fluxo n8n para aquele chamado e apresenta o estado de busca no modal
- **AND** impede disparos duplicados enquanto a mesma solicitação estiver em andamento

#### Scenario: Usuário sem permissão tenta consultar

- **WHEN** o usuário não é técnico, não está associado ao chamado conforme as regras atuais ou o atendimento está encerrado
- **THEN** a ação fica indisponível e uma chamada direta à operação é recusada antes de acionar o n8n

### Requirement: Modal de sugestões de solução

O sistema MUST apresentar o resultado no modal **Solução sugerida** vinculado ao chamado consultado e preservar o rascunho, o status e a solução gravada do atendimento.

#### Scenario: Fluxo retorna sugestões

- **WHEN** o fluxo retorna uma ou mais sugestões válidas
- **THEN** o modal mostra o chamado, as sugestões e seus passos numerados quando fornecidos
- **AND** mostra a categoria e o chamado de referência somente quando disponíveis e autorizados
- **AND** orienta o técnico a validar o procedimento e permite fechar o modal

#### Scenario: Fluxo não retorna resultados ou falha

- **WHEN** o fluxo retorna uma lista vazia, uma resposta inválida ou falha por indisponibilidade ou tempo limite
- **THEN** o modal distingue ausência de resultados de falha e permite fechar ou tentar novamente
- **AND** resultados de uma consulta anterior não são mostrados como resposta da atual

#### Scenario: Técnico muda de chamado durante a busca

- **WHEN** a resposta chega depois que o técnico mudou de chamado ou encerrou a sessão
- **THEN** o resultado da solicitação anterior é descartado pela interface
