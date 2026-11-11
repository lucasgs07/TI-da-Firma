# Proposal

## Why

Gestores ainda não dispõem de uma visão consolidada da evolução e da conclusão de chamados e tarefas, e as tarefas não podem ser acompanhadas em um fluxo visual adaptável às equipes. Esta mudança amplia as capacidades operacionais previstas para o MVP com métricas verificáveis e um quadro Kanban, mantendo autorização, integridade e regras de negócio no Xano.

## What Changes

- Introduz um dashboard gerencial que consolida chamados e tarefas, apresentando abertos, concluídos e atrasados, tempo médio de resolução, conclusões por equipe e colaborador e evolução mensal.
- Define produtividade como volume de demandas concluídas no período, discriminando chamados e tarefas para evitar somar unidades diferentes sem transparência.
- Define prazo/SLA de chamados calculado no backend por prioridade (Alta 12h, Média 36h, Baixa 50h), contando horas de dias úteis e pausando fins de semana e feriados nacionais brasileiros; tarefas continuam usando o campo `prazo` existente.
- Introduz um Kanban em que cada equipe/departamento configura colunas e etapas e movimenta tarefas; tarefas compartilhadas aparecem uma vez em cada quadro dos departamentos responsáveis, com etapa independente por quadro.
- Atribui a produtividade individual de cada tarefa concluída a quem a concluiu, uma única vez; para produtividade por equipe, conta a tarefa uma vez em cada departamento responsável, sem somar subtotais de equipe como total organizacional.
- Exige que consultas, agregações, transições de etapa e autorização sejam garantidas por endpoints e regras no Xano; a interface Reflex apresenta o estado e solicita as operações.
- Coordena a implementação com a mudança ativa `estrutura-inicial-do-modulo-de-chamados`, que já prevê tarefas e um dashboard básico, evitando duplicar essas entregas.
- Adia limites WIP para uma mudança futura; não haverá configuração, interface ou enforcement de capacidade por etapa nesta entrega.

## Capabilities

### New Capabilities

- `productivity-dashboard`: indicadores agregados de chamados e tarefas para gestores, com recorte temporal e de acesso por perfil/departamento.
- `task-kanban`: quadro operacional de tarefas com etapas configuráveis, transições e filtros.

### Modified Capabilities

Nenhuma capacidade durável existente tem requisitos diretamente relacionados a dashboard ou Kanban. Os requisitos planejados de tarefas e indicadores na mudança ativa de chamados deverão ser considerados durante a implementação para manter um único fluxo operacional.

## Impact

- **Xano e modelo de dados:** endpoints e regras de negócio para agregações gerenciais, configuração de SLA por prioridade e configuração de quadros por equipe/departamento; transições precisam verificar permissões no servidor.
- **Reflex:** novas interfaces de dashboard e Kanban, chamadas autenticadas, filtros, estados de carregamento/erro e atualização visual após operações confirmadas pelo Xano.
- **Acesso e segurança:** manter escopo de gestores por departamento e de administradores conforme política do backend; não expor dados de outras equipes por filtros manipuláveis no cliente.
- **Dados históricos:** tempo de resolução depende de datas consistentes de criação e conclusão; a precisão disponível e a retenção de histórico devem ser avaliadas antes de definir os cálculos.
- **Dependências de produto:** definir os valores e a vigência dos SLAs por prioridade, o período padrão dos indicadores e como as etapas de tarefas se relacionam com os status compartilhados existentes.
