# Visão Geral do Projeto

## 1. Descrição

A Plataforma de Gestão Interna Empresarial é uma aplicação web destinada a centralizar e organizar processos, recursos e solicitações de uma empresa. O sistema reunirá o gerenciamento de usuários, departamentos, chamados, ativos/equipamentos e tarefas, com diferentes níveis de acesso e um painel de acompanhamento.

O projeto será desenvolvido como um Produto Mínimo Viável (MVP), priorizando um fluxo completo e integrado em vez de tentar reproduzir um sistema corporativo completo.

## 2. Problema

Informações e solicitações empresariais podem ficar distribuídas em diferentes canais, dificultando o acompanhamento de chamados, equipamentos, tarefas e responsabilidades. A plataforma pretende centralizar essas informações em um único ambiente.

## 3. Objetivo

Criar uma plataforma web que permita registrar, acompanhar e organizar chamados, ativos e tarefas, relacionando essas informações aos usuários e departamentos e disponibilizando indicadores para gestores.

## 4. Público-alvo e perfis de usuário

- **Funcionário:** abre e acompanha suas solicitações e consulta as informações permitidas.
- **Técnico:** atende chamados, registra interações e trabalha com ativos e tarefas atribuídas.
- **Gestor:** acompanha chamados, atividades e ativos dentro do contexto e das permissões autorizadas.
- **Administrador:** gerencia o ambiente de forma geral.

As permissões detalhadas de cada perfil deverão ser validadas pela equipe antes da implementação.

## 5. Escopo do MVP

O MVP prevê os seguintes módulos:

- Autenticação e controle de acesso.
- Gerenciamento de usuários e departamentos.
- Gerenciamento de chamados.
- Gerenciamento de ativos/equipamentos.
- Gerenciamento de tarefas.
- Dashboard gerencial.

### 5.1 Fluxo principal

1. Um funcionário abre um chamado.
2. O sistema registra o chamado no Xano.
3. A IA poderá sugerir uma categoria e uma prioridade.
4. Um técnico recebe o chamado.
5. Um ativo pode ser associado ao chamado.
6. O técnico registra interações e/ou cria ou recebe uma tarefa.
7. O chamado é atualizado.
8. O gestor acompanha os indicadores no dashboard.

A IA deve apoiar o processo, sem substituir a decisão do usuário responsável.

## 6. Funcionalidades de IA previstas

- Classificação automática ou sugestão de categoria de chamado.
- Sugestão de prioridade com base na descrição e no contexto.
- Sugestão de procedimentos para resolução.
- Resumo do histórico de um chamado.

A implementação dessas funcionalidades será priorizada conforme o tempo disponível. A documentação original prevê implementar a IA depois que o fluxo básico estiver estável.

## 7. Dashboard gerencial

O dashboard deverá apresentar, no mínimo, indicadores relacionados a:

- Chamados abertos, em atendimento e resolvidos.
- Chamados por categoria e prioridade.
- Tarefas pendentes e atrasadas.
- Quantidade de ativos por status.
- Indicadores por departamento.
- Resumo das atividades recentes.

Os indicadores e seus critérios exatos deverão ser refinados durante a especificação das funcionalidades.

## 8. Tecnologias e ferramentas

- **Xano:** backend, banco de dados, autenticação, APIs e regras de negócio.
- **OpenSpec + IA:** especificação e desenvolvimento assistido das funcionalidades.
- **Frontend web:** Streamlit ou Reflex; a escolha ainda precisa ser definida pela equipe.
- **GitHub:** versionamento, branches, issues, pull requests e documentação.
- **API externa:** será definida durante a arquitetura, conforme a necessidade do MVP.
- **Deploy:** ambiente de produção a ser definido pela equipe conforme as opções trabalhadas na disciplina.

## 9. Critérios de conclusão do MVP

O MVP será considerado pronto quando:

- O usuário conseguir fazer login.
- As permissões impedirem acessos indevidos.
- Um funcionário conseguir abrir um chamado.
- O chamado ficar persistido no Xano.
- Um técnico conseguir visualizar e atualizar um chamado.
- As interações ficarem registradas.
- Um chamado puder ser associado a um ativo.
- Tarefas puderem ser criadas e atribuídas.
- O dashboard apresentar indicadores básicos.
- Pelo menos uma funcionalidade de IA estiver integrada ao fluxo.
- O sistema estiver publicado e puder ser testado por usuários.

## 10. Restrições, riscos e prioridades

- O projeto é um MVP, não um sistema corporativo completo.
- O fluxo de chamados deve ser priorizado antes de funcionalidades secundárias.
- A IA deve ser implementada somente depois de o fluxo básico estar estável.
- A equipe deve manter a documentação e as issues atualizadas.
- Devem ser realizados commits e pull requests frequentes.
- A etapa final deve reservar tempo para testes, deploy e validação.

## 11. Planejamento de referência

O planejamento original estima aproximadamente 10–12 semanas, com três integrantes e carga média de 6–8 horas por pessoa por semana.

As etapas previstas são:

1. Ideação e requisitos.
2. Arquitetura e documentação.
3. Backend e Xano.
4. Perfis e autorização.
5. Frontend.
6. Funcionalidades de IA e OpenSpec.
7. Integração.
8. Testes.
9. Deploy.
10. Validação e apresentação.

O cronograma é uma estimativa e poderá ser ajustado pela equipe.

## 12. Decisões pendentes

- Escolher entre Streamlit e Reflex para o frontend.
- Definir a API externa, caso seja necessária.
- Definir o ambiente de deploy.
- Validar o modelo de dados, incluindo chaves primárias, chaves estrangeiras, cardinalidades e campos.
- Refinar as permissões por perfil.
- Priorizar quais funcionalidades de IA serão entregues dentro do prazo do MVP.

## 13. Princípios de desenvolvimento

- Desenvolver incrementalmente, com foco no MVP.
- Revisar requisitos e especificações antes de implementar cada mudança.
- Preservar as regras de acesso e a autorização no backend.
- Evitar implementar funcionalidades fora do escopo sem aprovação da equipe.
- Validar as decisões de arquitetura e modelagem com o grupo.
