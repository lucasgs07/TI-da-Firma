# Proposal

## Why

O técnico precisa consultar possíveis soluções durante o atendimento sem sair do detalhe do chamado. A sugestão da IA oferece um ponto de partida para o diagnóstico, que o técnico valida antes de registrar a solução final.

## What Changes

- Adicionar o botão **Sugerir solução** ao lado de **Solução final** no painel de atendimento técnico.
- Acionar o fluxo n8n sob demanda e apresentar as sugestões em um modal, seguindo as imagens enviadas. Exibir passos numerados e chamados de referência quando disponíveis e autorizados.
- Manter a revisão humana e a gravação pelo fluxo atual de atendimento.

## Capabilities

### New Capabilities

- `ticket-solution-suggestions` — consulta e exibição de sugestões de solução para técnicos autorizados.

### Modified Capabilities

## Impact

- O Reflex ganha o botão, o modal e estados de busca, ausência de resultados e erro.
- O Xano autoriza a operação e intermedeia a integração com o n8n. A proposta usa o modelo atual de chamados.
- O endereço do webhook, a autenticação e exemplos de entrada e saída do fluxo precisam ser confirmados no apply.
