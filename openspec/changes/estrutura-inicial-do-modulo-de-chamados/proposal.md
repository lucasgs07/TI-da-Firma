# Proposta

## Por que

A operação interna da empresa está dispersa em diferentes canais e registros, o que dificulta o acompanhamento de solicitações, responsabilidades e indicadores de atendimento. A estrutura inicial do módulo de chamados centraliza o ciclo de vida das demandas internas em uma única aplicação, com foco no MVP e no fluxo de abertura, atendimento, acompanhamento e gestão operacional.

Essa mudança é necessária agora porque o processo de chamados é o núcleo do valor do produto. Sem esse fluxo estabelecido, os demais módulos de ativos, tarefas e painel gerencial não conseguem operar com consistência e rastreabilidade.

## O que muda

- Cria a base do módulo de chamados para o MVP, incluindo abertura, consulta, atualização e histórico de atendimento.
- Inclui uma tela autenticada de abertura de chamados em Reflex, com título, descrição, categoria e prioridade, identificação somente para leitura do usuário autenticado e retorno de confirmação após o registro.
- Define o fluxo principal de trabalho para funcionários, técnicos e gestores, com responsabilidade clara por solicitante e responsável.
- Permite associar chamados a ativos e registrar interações do atendimento em um histórico estruturado.
- Estabelece a base para criação e acompanhamento de tarefas vinculadas ao processo de atendimento.
- Gera os requisitos mínimos para os indicadores gerenciais de chamados, como quantidade por status, categoria e prioridade.
- Mantém a IA como apoio ao processo, sem substituir a decisão do usuário responsável.
- Registra decisões técnicas pendentes, especialmente sobre permissões, status, categorias, prioridades e modelagem do banco no Xano.

## Capacidades

### Novas capacidades
- `ticket-management`: gerenciamento do ciclo de vida de chamados internos, incluindo abertura, atribuição, atualização de status, interações, associação a ativos e acompanhamento de indicadores básicos do atendimento.

### Capacidades modificadas
- Nenhuma capacidade existente foi identificada no projeto para alteração de requisitos nesta etapa.

## Impacto

- Backend em Xano: persistência de chamados, interações, agentes envolvidos e regras básicas de status.
- Integração da tela com os endpoints autenticados existentes para consultar categorias e prioridades e criar chamados; o Xano continua definindo o solicitante e o status inicial.
- Banco de dados e regras de negócio: estruturação inicial de usuários, departamentos, perfil, chamado, interação, ativo e tarefa.
- Autorização e controle de acesso: além da autenticação, o módulo exigirá regras de visibilidade e permissão por perfil.
- Frontend Reflex: reutilização da sessão implementada no pacote `TI_da_Firma` para proteger a tela e exibir o nome do usuário autenticado.
- Dashboard gerencial: indicadores do módulo de chamados alimentam painéis iniciais de acompanhamento por gestor.
- IA: classificação e sugestão de prioridade continuam sendo apoiadas como recursos assistivos, e não como substituição da decisão humana.
