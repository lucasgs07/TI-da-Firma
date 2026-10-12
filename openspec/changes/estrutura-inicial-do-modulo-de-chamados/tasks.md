# Tarefas

## 1. Fundamentos do módulo de chamados

- [ ] 1.1 Definir a estrutura inicial de usuários, departamentos e perfis no Xano e validar a matriz mínima de acesso para funcionário, técnico, gestor e administrador. Verificação: confirmar que a autenticação e os metadados do usuário suportam o fluxo do MVP e que nenhum papel não autorizado pode alcançar ações de chamados.
- [ ] 1.2 Modelar a entidade base de chamado com campos essenciais para solicitante, responsável, categoria, prioridade, status, descrição e data de criação, mantendo o escopo compatível com a documentação do MVP. Verificação: confirmar que o registro suporta o fluxo de funcionário para técnico sem introduzir complexidade fora do escopo.
- [ ] 1.3 Modelar o histórico de interações e a relação com ativos para garantir rastreabilidade operacional. Verificação: confirmar que cada chamado pode registrar interações e, quando relevante, vincular-se a um ativo.

## 2. Fluxo principal de atendimento

- [ ] 2.1 Implementar a criação de chamados por funcionários, com persistência e visualização mínima do registro para o solicitante. Verificação: concluir um fluxo de criação bem-sucedido no aplicativo e confirmar que o chamado foi salvo no Xano.
- [ ] 2.2 Implementar a visualização e atualização de chamados por técnicos, incluindo atribuição, mudança de status e registro de interações. Verificação: atribuir um chamado a um técnico e confirmar que as mudanças de status e as observações ficam visíveis no histórico.
- [ ] 2.3 Validar o fluxo completo de abertura, atribuição e atualização do chamado, incluindo cenário de responsabilidade e histórico. Verificação: percorrer o processo completo desde a criação pelo funcionário até a resolução técnica e confirmar o estado final no banco de dados.

## 3. Ativos, tarefas e indicadores

- [ ] 3.1 Implementar a associação de um chamado a um ativo relevante, respeitando as regras mínimas do MVP. Verificação: vincular um chamado a um ativo e confirmar que a relação aparece no contexto do ticket.
- [ ] 3.2 Implementar a criação e atribuição de tarefas dentro do processo de atendimento, com acompanhamento de pendência e atraso. Verificação: criar uma tarefa, atribuí-la a um usuário e confirmar que ela aparece na lista operacional.
- [ ] 3.3 Implementar o dashboard básico de chamados, incluindo contagem por status, categoria, prioridade e atividade recente. Verificação: confirmar que o painel reflete os dados reais dos chamados e que os totais coincidem com os registros persistidos.

## 4. IA, validação e entrega

- [ ] 4.1 Integrar a funcionalidade mínima de IA para sugestão de categoria e prioridade, mantendo a decisão humana como ponto final. Verificação: confirmar que o sistema sugere valores, mas permite sobrescrita explícita antes do salvamento ou encerramento.
- [ ] 4.2 Validar segurança e permissões no backend para todos os perfis do módulo de chamados. Verificação: testar acessos negados e confirmar que usuários não autorizados não conseguem ler ou alterar registros de chamados.
- [ ] 4.3 Executar revisão final do MVP do módulo, incluindo testes de criação, acompanhamento, associação, tarefa e dashboard, e registrar pendências para refinamentos futuros. Verificação: concluir a checklist operacional completa e documentar decisões em aberto antes do arquivamento da mudança.

## Acompanhamento do fluxo de trabalho

- Preparar a revisão final da mudança com a equipe, confirmar as decisões pendentes e validar se o escopo do MVP foi respeitado antes do próximo ciclo de desenvolvimento.
- Caso a mudança seja aprovada, avançar para o próximo módulo do produto sem ampliar o escopo para funcionalidades fora do MVP.
