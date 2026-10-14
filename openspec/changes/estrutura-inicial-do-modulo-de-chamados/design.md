# Design

## Contexto

Consulte a proposta em [proposal.md](proposal.md). Esta mudança define a arquitetura inicial do módulo de chamados para o MVP, com Xano como responsável pelo backend, banco de dados, autenticação, APIs e regras de negócio. O frontend será implementado em Reflex, conforme a decisão já adotada pela equipe.

A aplicação Reflex atual está no pacote `TI_da_Firma`. O pacote já contém login, validação da sessão por `auth/me`, estado seguro do usuário em `AuthState` e o cliente HTTP `xano_client.py`; ainda não contém a tela nem chamadas de categorias, prioridades ou criação de chamados.

O Xano exportado já contém endpoints autenticados para consultar categorias e prioridades e criar chamados. O endpoint de criação aceita `titulo`, `descricao`, `categoria_chamado_id` e `prioridade_id`; define o status inicial e obtém o solicitante a partir da identidade autenticada. Consulte a especificação em [specs/ticket-management/spec.md](specs/ticket-management/spec.md) para os comportamentos esperados da tela.

## Objetivos / Não objetivos

**Objetivos:**
- Criar um ciclo de vida mínimo de chamados com responsabilidade clara e rastreabilidade.
- Apoiar o fluxo operacional entre funcionário, técnico e gestor sem expandir o escopo além do MVP.
- Manter todas as regras de acesso reforçadas no backend, independentemente da interface.
- Disponibilizar um painel mínimo que reflita o estado do processo de chamados.
- Integrar a tela de abertura à sessão Reflex existente e aos contratos autenticados do Xano, sem duplicar autenticação nem permitir edição local da identidade do solicitante.

**Não objetivos:**
- Personalização avançada de processos corporativos, mecanismo de SLA ou aprovação complexa.
- Anexos de documentos, assinaturas ou notificações sofisticadas.
- Automação completa de decisão por IA.
- Auditoria profunda além do histórico básico de interações.
- Implementar login ou persistência de sessão novamente.
- Associar um ativo durante a abertura: embora `chamado.ativo_id` exista no esquema, o endpoint atual de criação não aceita `ativo_id`; essa associação exige decisão e alteração separada do contrato do Xano.

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

### 8. A tela reutilizará a sessão autenticada existente
A página de abertura deve validar a sessão pela guarda já usada no pacote `TI_da_Firma` e ler o nome do usuário do perfil seguro em `AuthState`. O controle de acesso definitivo continua no Xano; a interface pode ocultar ou bloquear a ação para perfis sem permissão, mas não substitui a validação do endpoint.

**Alternativas consideradas:**
- Criar uma segunda implementação de login ou manter uma identidade independente na tela, o que duplicaria responsabilidades e poderia divergir da sessão validada.
- Usar apenas o nome informado em um campo editável, o que não comprovaria quem solicitou o chamado.

### 9. A tela usará os endpoints de consulta e criação já exportados
O cliente Reflex deve enviar o token existente no cabeçalho `Authorization: Bearer <token>` ao consultar categorias e prioridades e ao criar o chamado. O formulário envia somente os quatro campos aceitos pelo endpoint; identidade do solicitante e status inicial permanecem sob responsabilidade do Xano.

**Alternativas consideradas:**
- Enviar `solicitante_id` ou `status_chamado_id` a partir do navegador, o que permitiria adulterar valores que o servidor já deriva com segurança.
- Criar endpoints duplicados ou alterar o esquema do banco sem necessidade demonstrada pelo contrato atual.

### 10. A validação visual espelhará os limites aceitos pelo Xano
A interface pode orientar o usuário antes do envio, mas a validação de entrada no Xano permanece autoritativa. Título e descrição são obrigatórios e respeitam os limites definidos no endpoint; categoria e prioridade devem corresponder a registros retornados pelos endpoints de consulta.

**Alternativas consideradas:**
- Tratar a validação do frontend como garantia de integridade, o que seria contornável.
- Fixar opções de categoria ou prioridade na aplicação, o que ficaria desatualizado em relação ao Xano.

## Riscos e trade-offs

- [Risco de escopo] → Se a equipe tentar finalizar toda a taxonomia antes da implementação, o MVP pode travar. Mitigação: definir um conjunto mínimo operacional de status, categorias e prioridades e ajustar depois, se necessário.
- [Risco de segurança] → Se a autorização for implementada apenas na interface, usuários poderão acessar dados incorretamente. Mitigação: reforçar todas as regras de acesso no backend.
- [Ambiguidade do modelo de dados] → O modelo de chamados é intencionalmente amplo, mas ainda precisa de validação sobre campos e cardinalidade exatas. Mitigação: manter o design no nível conceitual e validar o modelo físico antes da implementação no Xano.
- [Desvio da IA] → Se a camada de IA mudar rapidamente, o fluxo de negócio pode se tornar inconsistente. Mitigação: manter a IA consultiva e adiar automação mais profunda até que o fluxo principal esteja estável.
- [Falha ou indisponibilidade dos endpoints de consulta] → O formulário pode não obter categorias ou prioridades. Mitigação: mostrar estado de carregamento, erro recuperável e ausência de opções; não enviar valores fictícios nem simular sucesso.
- [Diferença entre perfil exibido e autorização] → O perfil mantido no navegador pode estar desatualizado ou ser adulterado. Mitigação: usar a identidade local apenas para apresentação e manter a autorização no Xano, que valida a sessão e o perfil em cada requisição.

## Plano de migração

Para a tela de abertura não está prevista migração de esquema nem alteração remota no Xano, pois os campos e endpoints necessários ao envio já existem. A implementação deverá:

1. Reutilizar a sessão validada por `AuthState`.
2. Estender o cliente Xano com consultas autenticadas de categorias e prioridades e o envio do formulário.
3. Adicionar a página protegida em Reflex com estados de carregamento, erro, ausência de opções e confirmação.
4. Validar a submissão com o contrato exportado e confirmar que o solicitante e o status vêm da resposta do Xano.

O rollback desta tela deve limitar-se à rota, aos componentes e às chamadas adicionadas ao cliente; não deve exigir reversão de esquema ou afetar a sessão de login existente.

## Perguntas em aberto

- Lista exata de status, categoria e prioridade para chamados.
- Matriz exata de permissões por perfil e papel.
- Detalhes finais do esquema no Xano: nomes, chaves e cardinalidades.
- Se todas as tarefas devem estar vinculadas a um chamado ou podem existir independentemente em versões futuras.
- Se a associação opcional de um ativo deve acontecer já na abertura. Esta proposta não inclui o campo porque o endpoint `POST chamado` atual não o aceita; incluí-lo exige ampliar e validar o contrato do backend antes da implementação.

Essas questões são deixadas em aberto porque não alteram o comportamento de negócio nem a divisão de tarefas do MVP, desde que o design continue centrado no fluxo principal de chamados.
