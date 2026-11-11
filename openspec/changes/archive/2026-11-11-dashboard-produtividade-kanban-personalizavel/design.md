# Design

## Context

Consulte [proposal.md](proposal.md) para a motivação e [specs/productivity-dashboard/spec.md](specs/productivity-dashboard/spec.md) e [specs/task-kanban/spec.md](specs/task-kanban/spec.md) para o contrato de comportamento.

O frontend está no pacote `TI_da_Firma` e já protege páginas com a sessão autenticada. O cliente Xano atual expõe operações de chamados, mas ainda não integra métricas gerenciais ou tarefas no frontend. No Xano exportado, tarefas têm responsável, prioridade, prazo, conclusão e um `status_chamado_id` compartilhado; chamados têm `created_at` e `resolvido_em`, mas a listagem pública atual não retorna `created_at` nem identifica quem resolveu. Há um endpoint de carga atual de técnicos, não de produtividade concluída.

O modelo exportado é uma representação local do Xano; alterações remotas não são presumidas. O dashboard e o Kanban atravessam o frontend, endpoints, autorização e estrutura de dados, portanto regras e agregações não podem depender somente do cliente.

Uma leitura somente de metadados do workspace Xano `147362` confirmou que já existem consultas/criação de tarefas e `helpdesk/metrics/technicians`. Esse endpoint existente mede carga atual (`tickets_assigned`, `tickets_pending`, `tasks_assigned`, `tasks_pending`), não produtividade concluída. A definição remota de tarefa também inclui `responsaveis_ids` e centraliza escopo na função `helpdesk/access/task_access`; a cópia em `database/xano-export/` está desatualizada em relação a esses contratos. A mudança ativa de chamados ainda tem pendentes as tarefas 3.2 (tarefas) e 3.3 (dashboard básico). A implementação deve integrar os fluxos de tarefa e o dashboard previsto, reutilizar as APIs remotas existentes quando cabível, estender o painel sem duplicá-lo e criar apenas contratos para capacidades ainda ausentes, sincronizando o export local somente após revisão e autorização apropriadas.

## Goals / Non-Goals

**Goals:**

- Calcular métricas no Xano, com filtros de período e dados de chamados/tarefas identificáveis separadamente.
- Respeitar o escopo de departamento dos gestores e o escopo administrativo já aplicado pelo backend.
- Permitir quadros e etapas independentes por equipe, sem transformar colunas de tarefa em status globais de chamado.
- Validar no backend autorização e transições de etapa.
- Preparar uma evolução de esquema não destrutiva e coordenada com a mudança ativa do módulo de chamados.

**Non-Goals:**

- Criar uma camada de BI ou exportação de relatórios.
- Alterar permissões por perfil além das operações explicitamente necessárias para consulta, configuração e movimentação.
- Definir valores de SLA, calendário de expediente ou metas de produtividade sem validação do negócio.
- Sincronizar alterações locais de Xano automaticamente com o workspace remoto.

## Decisions

### 1. Agregações e autorização permanecem no Xano

Criar operações autenticadas para fornecer resumos, séries mensais e resultados por colaborador/equipe. O backend aplica o escopo por perfil antes de agregar e retorna apenas os campos necessários ao painel; filtros recebidos do Reflex nunca ampliam acesso. O frontend apresenta os resultados e trata estados vazios e erros, sem recalcular métricas a partir de listas potencialmente incompletas.

**Alternativas consideradas:** agregar registros no Reflex, o que exporia detalhes desnecessários e produziria totais incorretos quando a listagem é paginada ou limitada por perfil; reutilizar o endpoint de carga atual, que conta itens atribuídos e pendentes, não conclusões no período.

### 2. Conclusão exige atribuição verificável e datas válidas

Usar as datas de criação e conclusão já existentes, com precisão e unidade declaradas na resposta. O backend registra o ator autenticado que concluiu a tarefa ou resolveu o chamado; cada conclusão individual é atribuída uma única vez a esse ator, nunca replicada entre todos os responsáveis. O chamado precisa registrar o técnico que efetivamente o resolveu, pois pode ter vários técnicos associados. Nas métricas de equipe, uma tarefa compartilhada conta uma vez para cada departamento distinto entre seus responsáveis; os subtotais departamentais não são somados como total organizacional.

**Alternativas consideradas:** contar cada responsável da tarefa ou técnico associado ao chamado como autor da conclusão, o que duplica produtividade; inferir o autor a partir do responsável atual, que pode não ser quem concluiu.

### 3. SLA é configurado por prioridade e o prazo é controlado no servidor

Adicionar `sla_horas` à configuração existente de `prioridade`, com Alta = 12, Média = 36 e Baixa = 50, após validar os registros existentes antes de preencher valores. O backend determina o prazo do chamado; o frontend não fornece prazo autoritativo. Gestores e administradores podem alterar a prioridade de chamados dentro do escopo de acesso já aplicado pelo backend; a nova duração integral é recalculada a partir do instante da alteração.

O relógio conta todas as horas de segunda a sexta-feira, inclusive à noite, pausando fins de semana e feriados nacionais definidos em lei federal. Não inclui Sexta-feira Santa, Carnaval ou Corpus Christi como feriados nacionais neste escopo. O calendário usa o fuso IANA `America/Sao_Paulo`; se o chamado for criado ou tiver prioridade alterada em dia não útil, a contagem começa às 00:00 de Brasília no próximo dia útil. Chamados sem `sla_horas` não entram como atrasados e a API sinaliza a ausência de configuração, sem mascará-la como zero.

**Alternativas consideradas:** receber prazo do navegador, que permitiria adulterar atrasos; classificar todos os chamados por uma duração fixa, ignorando prioridades e regras de expediente; inferir SLA sem configuração, gerando indicadores sem significado acordado.

### 4. Etapas do Kanban são distintas do status compartilhado de chamados e pertencem ao quadro

Cada departamento tem um quadro configurável, e a associação entre tarefa e departamento deve representar cada departamento distinto dos responsáveis atuais (usando `responsavel_id` como compatibilidade quando `responsaveis_ids` estiver vazio). Uma tarefa compartilhada aparece uma vez em cada quadro responsável; cada associação guarda sua própria etapa, de modo que mover o cartão em um quadro não altera os demais.

Modelar associação e etapa por quadro no backend, sem alterar o catálogo global `status_chamado`. Ao reatribuir uma tarefa, sincronizar suas associações departamentais: manter as existentes, criar associação para novo departamento na etapa inicial correspondente ao status operacional atual e remover a associação quando não houver mais responsável naquele departamento. Tarefas sem responsável permanecem sem associação automática. Uma conclusão é global: respeita o fluxo existente de tarefa (incluindo solução e data), e move todas as associações da tarefa para a etapa terminal configurada em cada quadro. A atualização de uma etapa não terminal continua sendo local ao quadro.

O acesso de gestor a um quadro compartilhado deve ser validado pela associação da tarefa com seu departamento, sem ampliar autorização para reatribuir ou alterar os demais dados da tarefa. A API do quadro retorna apenas os campos necessários ao cartão. A definição remota já centraliza acesso em `helpdesk/access/task_access`, cuja regra atual não autoriza gestores a operar tarefas com responsáveis fora do departamento; a nova operação deve validar seu escopo de quadro explicitamente.

A migração inicial cria associações por departamento distinto e mapeia o status operacional de cada tarefa para a etapa inicial de mesmo status; tarefas concluídas são posicionadas na etapa terminal de cada quadro. Não altera `status_chamado_id`, datas, solução ou histórico.

**Alternativas consideradas:** reutilizar diretamente `status_chamado` para colunas customizadas, o que mistura estados de tickets e tarefas e não representa fluxos por departamento; guardar uma única etapa na tarefa, o que faz a movimentação em uma equipe sobrescrever o fluxo das outras; guardar etapa apenas no frontend, o que impede consistência entre usuários.

### 5. Limites WIP ficam fora do escopo atual

Esta mudança não criará limites de trabalho em andamento, configuração de capacidade por etapa nem enforcement associado no backend ou no frontend. O tema poderá ser retomado em uma mudança futura após decisão de produto e validação de uma garantia segura de concorrência no backend.

**Evidência para futura retomada:** a documentação oficial do Xano descreve [Database Transaction](https://docs.xano.com/the-function-stack/functions/database-requests/database-transaction) com rollback de operações de banco e [Direct Database Query](https://docs.xano.com/the-function-stack/functions/database-requests/direct-database-query) para SQL, mas não especifica garantias de isolamento ou locks suficientes para provar enforcement concorrente de WIP. Nenhuma alteração remota foi feita para investigar esse ponto.

### 6. Período padrão e tendências

Disponibilizar filtro de datas e usar os últimos 12 meses como período inicial para as séries mensais. Agrupar criação pela data de criação e conclusão pela data de conclusão, mantendo chamados e tarefas em séries distintas. Exibir unidade de tempo consistente com a precisão persistida, sem fabricar granularidade que os dados não possuem.

**Alternativas consideradas:** fixar um único período sem opção de consulta, reduzindo a utilidade gerencial; combinar chamados e tarefas numa série única, dificultando comparação por unidade.

## Risks / Trade-offs

- [Datas históricas ou autores de conclusão ausentes] → Excluir registros sem dados suficientes dos cálculos e sinalizar ausência de amostra; não estimar valores.
- [Matriz de SLA acordada ainda não está configurada no workspace] → Não classificar chamados sem política efetivamente configurada como atrasados; validar valores e calendário na implantação.
- [Inconsistência entre etapas locais e conclusão global] → Manter etapa por associação de quadro, sincronizar somente a ação terminal global e testar reatribuições, conclusão, migração e acesso por departamento.
- [Sobrecarga ou exposição indevida em agregações] → Limitar resposta a dados agregados necessários, filtrar por escopo no servidor e testar gestores de departamentos diferentes.
- [Mudança em andamento já prevê dashboard básico e tarefas] → Integrar ou sequenciar as entregas com `estrutura-inicial-do-modulo-de-chamados`; não criar telas, consultas ou modelos duplicados.

## Migration Plan

1. Conferir o estado atual do workspace Xano e resolver diferenças entre o export local e o ambiente remoto; apresentar simulação de alterações e aguardar autorização antes de qualquer operação remota.
2. Acordar valores de SLA por prioridade, calendário aplicável, timezone de relatórios e responsáveis pela configuração dos quadros.
3. Projetar mudanças aditivas para SLA, autor da conclusão/resolução e associações tarefa-quadro por departamento; validar estratégia de compatibilidade.
4. Criar/atualizar endpoints Xano com autorização e testes de escopo antes de conectar as telas Reflex.
5. Migrar tarefas existentes para uma associação por departamento distinto de seus responsáveis, mapeando o status atual para a etapa inicial correspondente; preservar status, datas, solução e histórico, e manter tarefas sem responsável sem associação automática.
6. Publicar o dashboard e o Kanban após verificar os dados agregados e as transições. Manter disponíveis os fluxos existentes durante a adoção.
7. Em caso de rollback, desabilitar as novas rotas/telas e voltar às operações atuais; preservar registros e campos aditivos para correção posterior, sem exclusão sincronizada.

## Open Questions

Nenhuma pendência de produto bloqueia o escopo atual. Limites WIP estão adiados e exigirão uma decisão e validação técnica próprias se forem retomados.
