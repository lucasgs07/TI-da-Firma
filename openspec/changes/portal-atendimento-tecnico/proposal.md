# Proposal

## Why

O frontend atual oferece chamados apenas ao funcionário, impedindo o técnico de executar o atendimento pela aplicação. É necessário disponibilizar uma área operacional com visão de todos os chamados, contexto do solicitante e ações de atendimento, tomando a organização do GLPI como referência funcional.

## What Changes

- Exibir a área de atendimento após login de usuários com `perfil_id` 3.
- Permitir ao técnico listar e consultar todos os chamados, inclusive atribuídos a outros técnicos, resolvidos e fechados, conforme confirmação do solicitante desta mudança.
- Mostrar solicitante, técnicos associados, classificação, descrição, solução e histórico de comentários.
- Permitir autoassociação a chamados abertos, preservando associações existentes e a identidade obtida da sessão.
- Integrar comentários e atualização de status pelo técnico associado, incluindo conclusão com solução final obrigatória.
- Preservar os estados já aceitos pelo backend: `Em Análise`, `Em atendimento`, `Aguardando usuário`, `Resolvido` e `Fechado`.
- Manter os demais perfis e a área do funcionário com suas permissões atuais.

## Capabilities

### New Capabilities

- `technician-ticket-portal`: consulta global e atendimento autenticado de chamados pelo técnico.

### Modified Capabilities

Nenhuma. A capacidade `employee-ticket-portal` permanece exclusiva do funcionário; a mudança ativa `estrutura-inicial-do-modulo-de-chamados` é planejamento mais amplo, não uma funcionalidade concluída.

## Impact

- Frontend: `TI_da_Firma/TI_da_Firma.py`, `auth_state.py` e `xano_client.py`, com testes de integração e regressão correspondentes.
- Xano: consultas de chamado e interações, funções de escopo/leitura e contratos seguros de resposta; reutilizar os endpoints de assumir, comentar e atualizar operações.
- Persistência: reutilizar `chamado`, `chamado_tecnico`, `interacao_chamado`, `user` e os cadastros existentes, sem novas tabelas previstas.
- A ampliação da leitura técnica altera a política atual de fila aberta ou associação, sem ampliar automaticamente as permissões de escrita.
- A exportação local não comprova o estado remoto. Publicação no Xano exige simulação e autorização explícita antes de qualquer alteração remota.
- Premissas conservadoras: autoassociação somente em `Aberto`; comentários somente pelo técnico associado; chamados resolvidos/fechados mantêm o bloqueio operacional existente. Não se inclui reprodução integral do GLPI, anexos, SLA, reabertura, transferência, IA ou novos módulos.
