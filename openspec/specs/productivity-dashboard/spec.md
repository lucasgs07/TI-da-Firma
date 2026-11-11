# productivity-dashboard Specification

## Purpose

Permite que gestores acompanhem a evolução e a conclusão de chamados e tarefas por período, equipe e colaborador, com indicadores calculados a partir de dados autorizados e consolidados pelo backend.

## Requirements

### Requirement: Indicadores operacionais de chamados e tarefas
O sistema MUST apresentar separadamente os volumes de chamados e tarefas abertos, concluídos e atrasados, usando os estados e prazos válidos de cada tipo de demanda.

#### Scenario: Painel consolida os totais por tipo
- **WHEN** um gestor ou administrador consulta o dashboard
- **THEN** o sistema apresenta contagens de chamados e tarefas abertas e concluídas, discriminadas por tipo
- **AND** apresenta separadamente as contagens atrasadas, sem somar chamados e tarefas em um total ambíguo

#### Scenario: Demanda ainda não concluída ultrapassa o prazo
- **WHEN** um chamado ultrapassa o prazo derivado de seu SLA ou uma tarefa ultrapassa seu prazo e permanece não concluída
- **THEN** o sistema contabiliza a demanda como atrasada no tipo correspondente
- **AND** uma demanda concluída não é contabilizada como atualmente atrasada

#### Scenario: Prazo ou estado insuficiente para classificação
- **WHEN** uma demanda não tem prazo aplicável ou não pode ser classificada com os estados configurados
- **THEN** o sistema não a marca como atrasada nem como concluída por inferência
- **AND** a ausência de dados não é apresentada como uma métrica válida de zero atraso

### Requirement: Tempo médio de resolução
O sistema MUST apresentar o tempo médio entre criação e conclusão para demandas concluídas com datas válidas, separando chamados e tarefas e indicando a unidade e o período usado no cálculo.

#### Scenario: Cálculo do tempo médio
- **WHEN** o dashboard é consultado para um período com demandas concluídas e datas válidas
- **THEN** o sistema calcula a média do tempo decorrido entre criação e conclusão para cada tipo de demanda separadamente
- **AND** informa a unidade do resultado e considera somente registros com datas suficientes

#### Scenario: Nenhuma conclusão válida no período
- **WHEN** não há demandas concluídas com datas válidas para um tipo no período consultado
- **THEN** o sistema indica que não há dados para calcular aquela média
- **AND** não apresenta zero como se fosse uma média observada

### Requirement: Produtividade por equipe e colaborador
O sistema MUST medir produtividade pelo número de demandas concluídas no período e permitir visualizar resultados por equipe e colaborador, discriminando chamados e tarefas.

#### Scenario: Comparar conclusões no período
- **WHEN** um gestor ou administrador seleciona um período de consulta
- **THEN** o sistema apresenta quantidades de chamados e tarefas concluídos por equipe e colaborador durante esse período
- **AND** os resultados não são confundidos com a quantidade de trabalho atualmente atribuída

#### Scenario: Atribuir conclusão individual sem duplicidade
- **WHEN** uma tarefa com um ou vários responsáveis é concluída por um usuário autenticado
- **THEN** o backend atribui uma única conclusão individual ao usuário que realizou a conclusão
- **AND** não replica a conclusão para todos os responsáveis da tarefa

#### Scenario: Tarefa compartilhada em produtividade por equipe
- **WHEN** uma tarefa concluída tem responsáveis em mais de um departamento
- **THEN** ela conta uma vez na produtividade de cada departamento distinto envolvido
- **AND** o sistema não apresenta a soma dos subtotais departamentais como um total organizacional sem deduplicação

#### Scenario: Chamado resolvido por técnico
- **WHEN** um técnico autorizado resolve um chamado
- **THEN** o backend atribui a conclusão individual ao técnico que realizou a resolução
- **AND** não atribui automaticamente a conclusão a todos os técnicos associados ao chamado

#### Scenario: Usuário sem conclusão no período
- **WHEN** um colaborador não conclui demandas durante o período consultado
- **THEN** o sistema o representa com contagem zero ou o identifica explicitamente como sem conclusões, de forma consistente no relatório

### Requirement: Evolução mensal das demandas
O sistema MUST apresentar uma série mensal de criação e conclusão de chamados e tarefas, mantendo cada tipo de demanda identificável.

#### Scenario: Visualizar evolução mensal
- **WHEN** um gestor ou administrador consulta a evolução mensal
- **THEN** o sistema agrupa chamados e tarefas pela data de criação e pela data de conclusão, respectivamente
- **AND** apresenta as séries de criação e conclusão por mês sem misturar os tipos de demanda

#### Scenario: Mês sem movimentação
- **WHEN** não há criação ou conclusão de um tipo de demanda em um mês do intervalo apresentado
- **THEN** o sistema mantém o mês na série com valor zero para aquela categoria

### Requirement: Escopo de acesso dos indicadores
O sistema MUST permitir a consulta de indicadores somente a gestores e administradores autorizados e MUST aplicar no backend o escopo organizacional permitido ao solicitante.

#### Scenario: Gestor consulta indicadores
- **WHEN** um gestor consulta o dashboard ou altera filtros de equipe, colaborador ou período
- **THEN** o Xano limita os registros à equipe ou departamento que o gestor pode acessar
- **AND** os filtros enviados pelo cliente não ampliam esse escopo

#### Scenario: Administrador consulta indicadores
- **WHEN** um administrador autorizado consulta o dashboard
- **THEN** o sistema retorna os indicadores dentro do escopo administrativo permitido

#### Scenario: Perfil não autorizado tenta consultar indicadores
- **WHEN** um usuário sem permissão de gestão chama diretamente um endpoint de indicadores
- **THEN** o Xano nega a consulta sem expor dados agregados ou detalhados

### Requirement: Prazo de chamado derivado de SLA
O sistema MUST determinar no backend o prazo de um chamado usando a duração `sla_horas` configurada para sua prioridade antes de incluí-lo em indicadores de atraso.

#### Scenario: Matriz e calendário de SLA acordados
- **WHEN** o backend calcula o prazo de um chamado com prioridade Alta, Média ou Baixa
- **THEN** usa, respectivamente, 12, 36 ou 50 horas configuradas na prioridade
- **AND** conta horas de segunda a sexta-feira, inclusive à noite, pausando fins de semana e feriados nacionais definidos em lei federal no fuso `America/Sao_Paulo`
- **AND** não trata Sexta-feira Santa, Carnaval ou Corpus Christi como feriados nacionais neste escopo

#### Scenario: SLA iniciado ou alterado em dia não útil
- **WHEN** um chamado é criado em fim de semana ou feriado nacional, ou sua prioridade é alterada em um dia não útil
- **THEN** a contagem correspondente começa às 00:00 de Brasília no próximo dia útil
- **AND** uma alteração de prioridade recalcula o prazo integral conforme o novo nível de SLA

#### Scenario: Chamado recebe prazo conforme prioridade
- **WHEN** um chamado é criado com uma prioridade que possui SLA vigente
- **THEN** o backend determina e persiste ou calcula o prazo aplicável ao chamado
- **AND** o prazo não é aceito como valor autoritativo enviado pelo frontend

#### Scenario: Prioridade sem SLA configurado
- **WHEN** um chamado é criado ou alterado para uma prioridade sem política de SLA vigente
- **THEN** o backend não inventa um prazo nem classifica o chamado como atrasado
- **AND** informa a condição de configuração ausente conforme o contrato da operação

#### Scenario: Gestor ou administrador altera a prioridade
- **WHEN** um gestor ou administrador autorizado altera a prioridade de um chamado dentro do seu escopo de acesso
- **THEN** o backend recalcula o prazo integral a partir do instante da alteração, usando a nova prioridade e o calendário de SLA
- **AND** ignora qualquer prazo de SLA enviado pelo cliente

#### Scenario: Outro perfil tenta alterar a prioridade
- **WHEN** um técnico ou funcionário tenta alterar a prioridade do chamado
- **THEN** o backend nega a operação sem alterar a prioridade nem o prazo de SLA

#### Scenario: Prazo do chamado é ultrapassado
- **WHEN** o prazo de um chamado ainda não concluído é anterior ao instante atual
- **THEN** o backend o inclui na contagem de chamados atrasados
- **AND** exclui chamados concluídos da contagem atual de atrasos
