# Modelo de Domínio

## 1. Objetivo deste documento

Este documento descreve os principais conceitos do domínio da Plataforma de Gestão Interna Empresarial e os relacionamentos previstos entre eles, com base na documentação inicial do projeto.

Ele representa uma visão conceitual. Não define ainda o esquema físico do banco de dados, os tipos das colunas, os nomes definitivos de campos ou comandos SQL. Esses detalhes deverão ser validados pela equipe antes da implementação no Xano.

## 2. Entidades principais

### 2.1 Usuario

Representa uma pessoa que utiliza a plataforma, como funcionário, técnico, gestor ou administrador.

Responsabilidades conceituais:
- Identificar o usuário no sistema.
- Relacionar o usuário a um departamento e a um perfil.
- Permitir associar usuários a chamados, interações, ativos e tarefas conforme as regras de negócio.

### 2.2 Departamento

Representa uma unidade organizacional da empresa.

Responsabilidades conceituais:
- Agrupar usuários.
- Permitir relacionar ativos a uma área organizacional.
- Apoiar a visualização de indicadores por departamento.

### 2.3 Perfil

Representa o perfil de acesso atribuído a um usuário.

A documentação cita os perfis Administrador, Gestor, Técnico e Funcionário. As permissões específicas de cada perfil deverão ser definidas e validadas pela equipe.

### 2.4 Chamado

Representa uma solicitação ou ocorrência registrada na plataforma.

Responsabilidades conceituais:
- Registrar uma solicitação feita por um usuário.
- Ter um solicitante e, quando aplicável, um responsável.
- Ser classificado por categoria, status e prioridade.
- Possibilitar o registro de interações.
- Poder ser associado a um ativo.
- Apoiar o acompanhamento do atendimento e os indicadores do dashboard.

### 2.5 CategoriaChamado

Representa a categoria usada para classificar um chamado. A lista de categorias ainda deverá ser definida pela equipe.

### 2.6 StatusChamado

Representa o estado atual de um chamado. Os estados exatos e suas transições ainda deverão ser especificados.

A documentação cita indicadores de chamados abertos, em atendimento e resolvidos, mas não estabelece uma lista completa de status.

### 2.7 Prioridade

Representa o nível de prioridade atribuído a um chamado. Os níveis e critérios de classificação ainda deverão ser definidos.

A IA poderá sugerir uma categoria e uma prioridade, mas a decisão permanece com o usuário responsável.

### 2.8 InteracaoChamado

Representa uma interação ou registro relacionado ao atendimento de um chamado.

Responsabilidades conceituais:
- Relacionar uma interação a um chamado.
- Identificar o usuário que registrou a interação.
- Manter o histórico de atendimento.

### 2.9 Ativo

Representa um ativo ou equipamento gerenciado pela empresa.

Responsabilidades conceituais:
- Ser classificado por tipo e status.
- Poder ser relacionado a um usuário e a um departamento.
- Poder ser associado a um chamado, conforme o fluxo principal do produto.

A forma exata de associação entre ativo e chamado ainda deverá ser validada na modelagem definitiva.

### 2.10 TipoAtivo

Representa a classificação de um ativo ou equipamento.

As categorias concretas de tipo de ativo ainda não foram definidas na documentação inicial.

### 2.11 StatusAtivo

Representa o estado de um ativo. A lista de estados possíveis ainda deverá ser definida pela equipe.

### 2.12 Tarefa

Representa uma atividade que pode ser criada ou atribuída durante o trabalho da equipe.

Responsabilidades conceituais:
- Ser atribuída a um usuário.
- Permitir acompanhar tarefas pendentes e atrasadas no dashboard.

A documentação inicial não especifica todos os campos da tarefa nem se toda tarefa precisa estar vinculada a um chamado. Essa decisão deverá ser validada.

## 3. Relacionamentos iniciais

Os relacionamentos abaixo reproduzem o modelo inicial descrito na documentação do projeto:

- **Departamento 1:N Usuario:** um departamento pode estar relacionado a vários usuários.
- **Perfil 1:N Usuario:** um perfil pode estar atribuído a vários usuários.
- **Usuario 1:N Chamado (solicitante):** um usuário pode solicitar vários chamados.
- **Usuario 1:N Chamado (responsável):** um usuário pode ser responsável por vários chamados.
- **CategoriaChamado 1:N Chamado:** uma categoria pode classificar vários chamados.
- **StatusChamado 1:N Chamado:** um status pode estar associado a vários chamados.
- **Prioridade 1:N Chamado:** uma prioridade pode estar associada a vários chamados.
- **Chamado 1:N InteracaoChamado:** um chamado pode ter várias interações.
- **Usuario 1:N InteracaoChamado:** um usuário pode registrar várias interações.
- **Usuario 1:N Ativo:** um usuário pode estar relacionado a vários ativos.
- **Departamento 1:N Ativo:** um departamento pode estar relacionado a vários ativos.
- **TipoAtivo 1:N Ativo:** um tipo pode classificar vários ativos.
- **StatusAtivo 1:N Ativo:** um status pode estar associado a vários ativos.
- **Usuario 1:N Tarefa:** um usuário pode estar relacionado a várias tarefas.

## 4. Regras e pontos a validar

Antes da implementação, a equipe deverá validar:

- Chaves primárias e estrangeiras, campos e cardinalidades definitivas.
- Se os relacionamentos de solicitante e responsável em Chamado serão opcionais ou obrigatórios em cada etapa do fluxo.
- As permissões de cada perfil e o escopo de acesso de gestores e funcionários.
- A lista de categorias, status e prioridades de chamados.
- A lista de tipos e status de ativos.
- Como um ativo será associado a um chamado.
- Se tarefas terão vínculo com chamados e quais estados terão.
- Quais registros e alterações precisarão ser auditados em uma eventual expansão futura.

## 5. Itens previstos para depois do MVP

A documentação original cita como possíveis expansões:

- Permissao e PerfilPermissao.
- LogAuditoria.
- Notificações.
- Anexos.
- SLA.
- Integrações adicionais.

Esses itens não devem ser tratados como funcionalidades obrigatórias do MVP sem uma decisão explícita da equipe.

## 6. Observações

Este modelo é inicial e conceitual. Ele deve orientar a discussão e a especificação incremental, não substituir a validação do DER nem a definição final do banco de dados no Xano.
