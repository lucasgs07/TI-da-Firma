# Tasks

## 1. Confirmar contratos e preparar dados

- [x] 1.1 Comparar o escopo desta mudança com as tarefas 3.2 e 3.3 da mudança ativa `estrutura-inicial-do-modulo-de-chamados`; verificar os contratos locais e o workspace Xano em modo somente leitura e registrar o plano integrado sem duplicar APIs ou telas.
- [x] 1.2 Definir durações de SLA por prioridade, calendário aplicável, timezone de relatórios e comportamento quando a prioridade do chamado mudar; verificar a matriz aprovada e os cenários de cálculo antes de habilitar o indicador de atraso em produção.
- [x] 1.3 Definir o mapeamento dos status atuais para etapas iniciais por departamento e validar a atribuição de conclusões; verificar um plano de migração cobrindo tarefas existentes, tarefas sem responsável e dados históricos incompletos sem alterar registros.
## 2. Implementar contratos e métricas no Xano

- [ ] 2.1 Adicionar `sla_horas` à prioridade, preencher as durações somente após validar os registros existentes e implementar cálculo/recalculo de prazo no backend para criação e alteração autorizada da prioridade; testar calendário federal, dias não úteis, prioridade sem SLA, chamados concluídos, atraso e negação a perfis não autorizados, documentando contratos.
- [ ] 2.2 Registrar no backend o ator autenticado que efetivamente resolve chamados ou conclui tarefas e expor datas e atribuição necessárias em respostas seguras; testar resolução por técnicos associados, conclusão por um dos múltiplos responsáveis e verificar que tarefas sem datas suficientes não entram nas médias.
- [ ] 2.3 Criar endpoints gerenciais para contagens por tipo, tempo médio, conclusões por equipe/colaborador e séries mensais; testar períodos sem dados, filtros, escopo de gestor por departamento, acesso administrativo, atribuição individual a quem concluiu e contagem de tarefas compartilhadas sem somar subtotais departamentais, documentando os contratos.

## 3. Implementar quadros e transições no Xano

- [ ] 3.1 Modelar configurações de quadro, etapas e associações tarefa-quadro por departamento, permitindo etapas independentes para uma tarefa compartilhada; migrar status atual para etapa inicial equivalente, levar tarefas concluídas à etapa terminal e preservar status, prazos, solução e histórico, com tarefas sem responsáveis sem associação automática.
- [ ] 3.2 Implementar APIs autenticadas de consulta, configuração e filtros de quadro por responsável, departamento e prioridade; mostrar uma tarefa uma vez por departamento distinto dos responsáveis e testar escopo de gestores de departamentos diferentes, administradores e usuários atribuídos, documentando os contratos.
- [ ] 3.3 Implementar movimentação independente por associação de quadro; testar transições inválidas, conclusão global para todas as etapas terminais e reatribuição entre departamentos, documentando erros e respostas.

## 4. Integrar interfaces Reflex

- [ ] 4.1 Integrar o cliente autenticado com os endpoints de métricas e tarefas, validar respostas e tratar falhas sem apresentar dados antigos como atuais; cobrir validação e erros com testes e documentar as integrações.
- [ ] 4.2 Criar o dashboard gerencial com filtros de período, totais separados de chamados/tarefas, médias, produtividade e evolução mensal; testar estados sem dados e conferir os resultados da interface contra respostas do Xano.
- [ ] 4.3 Criar o quadro Kanban por equipe com etapas ordenadas, filtros e movimentação; confirmar que a posição só muda após sucesso do Xano e volta ao estado confirmado após falha, cobrindo o comportamento em testes da interface.
- [ ] 4.4 Criar controles de configuração de etapas para gestores do próprio departamento e administradores; testar ocultação/negação por perfil e escopo, e documentar o fluxo de configuração.

## 5. Validar integração e entrega

- [ ] 5.1 Executar validação integrada de métricas, acesso entre departamentos, migração de tarefas e mudanças de etapa; verificar consistência entre Xano e Reflex e registrar resultados, pendências e procedimento de rollback antes da liberação.

## Fora do escopo desta mudança

- Limites WIP por etapa, incluindo configuração, interface, enforcement no backend e testes de concorrência, ficam adiados para uma mudança futura.
