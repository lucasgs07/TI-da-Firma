# Design

## Contexto

Consulte a proposta em [proposal.md](proposal.md). Esta mudança define a arquitetura inicial do módulo de chamados para o MVP, com Xano como responsável pelo backend, banco de dados, autenticação, APIs e regras de negócio. O frontend será implementado em Reflex, conforme a decisão já adotada pela equipe.

A solução deve manter foco no fluxo completo do módulo de chamados: criação, atribuição, atualização, histórico de interações, associação com ativos, acompanhamento de tarefas e painel gerencial básico.

## Objetivos / Não objetivos

**Objetivos:**
- Criar um ciclo de vida mínimo de chamados com responsabilidade clara e rastreabilidade.
- Apoiar o fluxo operacional entre funcionário, técnico e gestor sem expandir o escopo além do MVP.
- Manter todas as regras de acesso reforçadas no backend, independentemente da interface.
- Disponibilizar um painel mínimo que reflita o estado do processo de chamados.

**Não objetivos:**
- Personalização avançada de processos corporativos, mecanismo de SLA ou aprovação complexa.
- Anexos de documentos, assinaturas ou notificações sofisticadas.
- Automação completa de decisão por IA.
- Auditoria profunda além do histórico básico de interações.

## Decisões

### 1. O ciclo de vida do chamado será modelado como um único registro com status e cadeia de responsabilidade
A entidade principal de chamado deve ser um único registro operacional que capture quem abriu a solicitação, quem é o responsável, qual é o status atual e qual categoria e prioridade pertencem ao chamado. Esse é o modelo mais simples para apoiar o ciclo de criação, atribuição e atualização descrito no MVP, sem sobrecarregar prematuremente o modelo de dados.

**Alternativas consideradas:**
- Várias tabelas para cada etapa do ciclo de vida, o que aumentaria a complexidade sem trazer valor real no MVP.
- Um fluxo baseado em texto livre sem status estruturado, o que comprometeria relatórios e painéis.

### 2. O histórico de interações será um registro separado em vez de sobrescrever os campos do chamado
O sistema deve manter as interações como um log relacionado de eventos. Isso preserva o histórico operacional que gestores e técnicos precisam seguir, ao mesmo tempo em que mantém o registro principal do chamado legível e enxuto.

**Alternativas consideradas:**
- Atualizar somente os campos principais do chamado, o que perderia a rastreabilidade.
- Utilizar event sourcing detalhado antes da validação do MVP, o que acrescentaria complexidade desnecessária.

### 3. A associação com ativos permanecerá como relacionamento direto com o chamado e não como fluxo completo de gestão de patrimônio
O design deve permitir vincular um ativo ao chamado quando houver relação direta com a solicitação, mas não deve modelar todo o ciclo de vida de ativos nesta mudança. Os dados de ativos continuam sendo um domínio de apoio ao processo de chamados e não o foco principal do MVP.

**Alternativas consideradas:**
- Expandir para uma gestão completa de equipamentos antes que o fluxo de chamados esteja estável.
- Tratar a relação como uma anotação isolada sem vínculo estruturado, o que enfraqueceria os relatórios.

### 4. As tarefas serão leves e operacionais, e não totalmente orientadas a projetos
As tarefas devem ser unidades operacionais pequenas, criadas ou atribuídas durante o fluxo de atendimento. Seu objetivo é acompanhar o trabalho e sustentar métricas no painel, e não substituir um sistema completo de gestão de projetos.

**Alternativas consideradas:**
- Construir hierarquias separadas de tarefas com dependências e marcos.
- Exigir que toda tarefa esteja vinculada a um chamado, o que seria restritivo demais para evoluções futuras.

### 5. A autorização reforçada no backend será a fonte da verdade
As permissões devem ser validadas no servidor em Xano, em vez de depender apenas de restrições na interface. Isso reduz o risco de bypass e mantém o modelo compatível com futuras mudanças de interface.

**Alternativas consideradas:**
- Confiar apenas na visibilidade da interface, o que não é seguro.
- Definir regras de ação somente no frontend, o que criaria comportamento inconsistente entre clientes.

### 6. A IA será consultiva e não bloqueante
Os recursos iniciais de IA devem sugerir categoria e prioridade com base na descrição do chamado, mas não devem tomar decisões irreversíveis sem aprovação humana. Isso está alinhado ao princípio do projeto de que a IA apoia o processo sem substituir os responsáveis humanos.

**Alternativas consideradas:**
- Classificação automática sem revisão.
- Atrasar todas as funcionalidades de IA até depois do MVP, o que diminuiria o valor do fluxo.

### 7. Os indicadores do dashboard serão intencionalmente básicos no MVP
O painel inicial deve focar em contagens e fatias por status que sejam fáceis de verificar e sustentadas pelo modelo de chamados. Isso mantém o design prático e ainda oferece visibilidade gerencial.

**Alternativas consideradas:**
- Uma camada analítica sofisticada antes de validar o fluxo.
- Métricas complexas sem uma definição compartilhada de status e categoria.

## Riscos e trade-offs

- [Risco de escopo] → Se a equipe tentar finalizar toda a taxonomia antes da implementação, o MVP pode travar. Mitigação: definir um conjunto mínimo operacional de status, categorias e prioridades e ajustar depois, se necessário.
- [Risco de segurança] → Se a autorização for implementada apenas na interface, usuários poderão acessar dados incorretamente. Mitigação: reforçar todas as regras de acesso no backend.
- [Ambiguidade do modelo de dados] → O modelo de chamados é intencionalmente amplo, mas ainda precisa de validação sobre campos e cardinalidade exatas. Mitigação: manter o design no nível conceitual e validar o modelo físico antes da implementação no Xano.
- [Desvio da IA] → Se a camada de IA mudar rapidamente, o fluxo de negócio pode se tornar inconsistente. Mitigação: manter a IA consultiva e adiar automação mais profunda até que o fluxo principal esteja estável.
- [Incerteza de frontend] → A decisão de framework já foi tomada; o design deve refletir a arquitetura com Reflex e não assumir outros caminhos. Mitigação: tratar a interface como implementação do modelo de negócio, sem introduzir alternativas de tecnologia.

## Plano de migração

Não é necessária uma migração de grande porte para este artefato de planejamento. A primeira implementação deve criar ou estender as entidades centrais no Xano em etapas:

1. Adicionar as estruturas de usuário, departamento, perfil e autenticação necessárias para o acesso.
2. Criar os registros centrais de chamado e interação.
3. Adicionar relações de ativos e tarefas como modelos de apoio.
4. Expor as métricas do dashboard com base nesses dados.
5. Validar com um fluxo de ponta a ponta focado em uma sequência real de abertura, atribuição e atendimento.

O design deve permitir rollback seguro ao reverter juntos o esquema de chamados e as telas do frontend, sem afetar módulos não relacionados.

## Perguntas em aberto

- Lista exata de status, categoria e prioridade para chamados.
- Matriz exata de permissões por perfil e papel.
- Detalhes finais do esquema no Xano: nomes, chaves e cardinalidades.
- Se todas as tarefas devem estar vinculadas a um chamado ou podem existir independentemente em versões futuras.

Essas questões são deixadas em aberto porque não alteram o comportamento de negócio nem a divisão de tarefas do MVP, desde que o design continue centrado no fluxo principal de chamados.
