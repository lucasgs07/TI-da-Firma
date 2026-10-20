# Tasks

## Encerramento da validação — 20/10/2026

O usuário confirmou que também realizou os testes restantes de permissões e entradas inválidas no backend e autorizou confirmar a validação. Os dez critérios ainda abertos foram encerrados com base nessa confirmação manual: 27/27 tarefas. Essa evidência foi relatada pelo usuário; o agente não executou nem observou esses testes manuais. Permanecem como evidências diretas do agente os testes automatizados, compilação, publicação e conferência das exportações já registrados. As seções seguintes preservam o histórico das pendências à época de cada etapa.

## Validação manual confirmada pelo usuário — 20/10/2026

O usuário informou que testou os fluxos e confirmou também a visualização em desktop/celular e a conclusão simultânea da mesma tarefa por dois responsáveis. Evidência manual relatada pelo usuário, sem observação direta pelo agente. Com a compilação e publicação já verificadas, foram concluídos os itens 3.4, 4.3 e 4.4. Os registros abaixo descrevem etapas anteriores e suas pendências à época.

Continuam abertos os critérios específicos de testes negativos e contratos backend dos itens 1.1–1.6, 1.8–1.10 e 4.2, não individualmente comprovados pelo relato geral dos fluxos. Progresso: 17 de 27 tarefas. O arquivamento permanece preparado até concluir esses critérios.

## 1. Políticas e contratos Xano

- [x] 1.1 Confirmar a referência existente de T.I. no cadastro e atualizar `get_actor_scope` com capacidades distintas para gestor T.I. e demais gestores; verificar testes de perfil/departamento ausente, ator adulterado e regressões de administrador/técnico/funcionário, documentando a matriz de acesso.
- [x] 1.2 Atualizar leitura gerencial em lista/detalhe de chamados, `require_ticket_read` e consultas de interações para abranger membros de qualquer perfil do próprio departamento e leitura global T.I.; testar IDs externos, histórico filtrado, chamados próprios, mudança de departamento e ausência de ampliação de escrita.
- [x] 1.3 Adequar `users/create` para gestor T.I. criar perfis 2/3/4 em departamentos permitidos e demais gestores somente perfil 4 próprio, com novo técnico obrigatório em T.I.; testar administrador negado ao gestor, departamento inválido/adulterado, e-mail duplicado, senha inválida e resposta sem segredos.
- [x] 1.4 Conferir os caminhos de cadastro existentes, incluindo `auth/signup`, para impedir criação de técnico fora de T.I. sem ampliar permissões; verificar testes de tentativa de contorno e preservar usuários legados sem migração automática.
- [x] 1.5 Adequar POST `/tarefa` e validação de atribuição em PATCH: gestor T.I. para técnico T.I., demais gestores para funcionário do próprio departamento; testar alvos incompatíveis/externos/alterados após seleção, chamado opcional e autoria/status adulterados, preservando outras operações existentes.
- [x] 1.6 Adequar o diretório paginado para os seletores autorizados e confirmar consultas de departamentos/perfis; testar filtros, páginas além da primeira, escopo departamental e projeções sem dados secretos, com contratos documentados.
- [x] 1.7 Manter as representações afetadas de `apis/`, `functions/` e `database/xano-export/` coerentes; verificar diff sem novas tabelas/colunas, exclusões de dados ou credenciais e registrar o impacto das permissões alteradas.
- [x] 1.8 Permitir GET de lista/detalhe de tarefas próprias ao funcionário e ajustar leitura gerencial aos responsáveis elegíveis; testar tarefa alheia, ID direto, paginação quando aplicável e que uma tarefa vinculada não libera acesso ao chamado.
- [x] 1.9 Estender conclusão em PATCH `/tarefa/{id}` ao funcionário responsável, exigindo solução, status configurado e data do servidor; testar solução vazia, ator incorreto, campos proibidos, repetição idempotente, imutabilidade e ausência de alteração do chamado vinculado, documentando o contrato.
- [x] 1.10 Publicar e validar o campo aditivo `responsaveis_ids`, helper compartilhado e os cinco endpoints de tarefas para todos os membros, preservando tarefas legadas; executar testes Xano de associado secundário, escopo integral do gestor, seleção inválida sem gravação parcial, duplicação e conclusão global, incluindo concorrência.

## 2. Cliente HTTP e estado Reflex

- [x] 2.1 Após os contratos locais do grupo 1, acrescentar ao cliente HTTP cadastro, criação, consulta e conclusão de tarefas, diretório paginado e opções de perfil/departamento; verificar método/caminho/payload, paginação completa, tratamento de falhas e ausência de logs de senha/token.
- [x] 2.2 Implementar estado gerencial e seleção das capacidades após `auth/me`, integrando leitura/abertura de chamados sem liberar eventos exclusivos de funcionário/técnico; testar login/restauração de ambos os tipos de gestor, alteração do cache local, logout e limpeza de dados ao mudar de perfil/departamento.
- [x] 2.3 Implementar eventos de cadastro de usuários com opções permitidas, técnico fixo em T.I. e limpeza de senha, e evento de tarefa com responsável elegível; testar negações, falhas de rede, campos preservados sem segredos, sessão expirada, bloqueio de envio simultâneo e confirmação apenas após sucesso.
- [x] 2.4 Documentar configuração, contratos e limitações do estado gerencial e executar regressões de autenticação, portal do funcionário e portal técnico; verificar que a documentação corresponde aos payloads exercitados pelos testes.
- [x] 2.5 Implementar estado de tarefas próprias do funcionário e envio da solução, com loading, erro, limpeza na sessão e recarga após sucesso; testar falha preservando solução, sessão expirada, tarefa alheia e bloqueio de envio duplo, sem liberar eventos de atendimento de chamados.
- [x] 2.6 Suportar listas de responsáveis no cliente e estado, com prioridade da lista nova e fallback legado; verificar testes dos dois perfis para associado secundário, conclusão global, seleção duplicada/inválida e preservação em falha.

## 3. Telas gerenciais

- [x] 3.1 Criar a entrada gerencial na home Reflex e seções de consulta/detalhe/histórico e novo chamado, respeitando leitura global T.I. ou departamental; verificar renderização, solicitante/status/classificação, ausência de ações técnicas e estados carregando/vazio/erro para os dois gestores.
- [x] 3.2 Criar formulário de usuário com nome/e-mail/senha inicial e perfil/departamento permitidos, sem opção administrador para gestores; verificar técnico fixo em T.I., gestor comum fixo em funcionário do próprio departamento, mensagens e ausência de senha em estado persistido.
- [x] 3.3 Criar Nova tarefa para todos os gestores, selecionando técnico T.I. ou funcionário do próprio departamento conforme o gestor; verificar diretório paginado, falta de responsáveis, campos opcionais, confirmação e rejeição de responsável que deixou de ser elegível.
- [x] 3.4 Compilar com `reflex compile --dry` conforme a skill de processos e validar visualmente desktop/móvel para gestor T.I. e de outro departamento; registrar resultados, incluindo regressão visual dos portais existentes, sem marcar a tarefa concluída se uma verificação não puder ser executada.
- [x] 3.5 Acrescentar Minhas tarefas ao portal do funcionário, com lista, detalhe e solução obrigatória para concluir; verificar vazio/erro, persistência após recarga, conclusão bloqueada sem solução e manutenção das telas de chamados sem ações de resolução.
- [x] 3.6 Separar Chamados e Minhas tarefas em telas distintas para técnicos e funcionários, incluindo tarefas próprias do técnico; verificar testes dos dois perfis para carregamento, conclusão e bloqueio de tarefas alheias, e compilar a nova rota Reflex.
- [x] 3.7 Permitir seleção de vários responsáveis elegíveis por checkboxes e apresentar seus nomes na lista/detalhe da tarefa; verificar o payload de todos os selecionados e compilar os componentes Reflex.

## 4. Publicação e integração autorizadas

- [x] 4.1 Comparar os contratos locais e remotos envolvidos, apresentar simulação restrita dos arquivos e impacto das permissões; verificar `xano workspace push --dry-run` antes de qualquer push e aguardar autorização explícita sem utilizar opções destrutivas.
- [x] 4.2 Após autorização, publicar somente os contratos revisados e conferir a exportação; executar testes Xano e requisições negativas para gestor comum atribuir a usuário inelegível/criar técnico ou gestor/acessar chamado externo, e funcionário consultar/concluir tarefa alheia ou resolver chamado, sem modificar dados fora do teste autorizado.
- [x] 4.3 Validar fluxos reais de ambos os gestores, incluindo criação de tarefa para técnico T.I. e para funcionário departamental; validar funcionário consultando e concluindo tarefa própria com solução obrigatória, sem resolver chamado. Conferir persistência e registrar evidências e pendências antes de arquivar.
- [x] 4.4 Executar nova simulação restrita da tabela, helper e cinco endpoints para múltiplos responsáveis, obter autorização específica, publicar e conferir exportação e persistência para todos os associados, sem excluir campos ou registros legados.

## Registro de implementação local — 20/10/2026

A revisão de vários responsáveis foi publicada após autorização explícita da simulação: campo adicional em `tarefa`, helper e cinco endpoints, sem exclusões. A exportação dos sete contratos foi conferida e sincronizada. Os cinco testes com mocks do helper passaram no Xano; 105 testes Python e compilação Reflex já haviam passado. As tarefas 1.10 e 4.4 continuam abertas pelas validações restantes de fluxos reais, persistência e concorrência; publicação e testes com mocks não comprovam essas etapas. Consulte `docs/portal-gerencial.md` para a saída e o impacto.

Após publicação autorizada, os 20 testes unitários das duas funções alteradas passaram no Xano. Foram preservadas as pendências de testes específicos dos endpoints, cadastro T.I. e verificação visual.

Implementação preparada, com 86 testes Python passando e compilação Reflex concluída. Os contratos dos itens 1.1 a 1.6, 1.8 e 1.9 foram publicados após autorização, mas os itens permanecem abertos por dependerem da confirmação do cadastro T.I. e/ou execução das validações específicas indicadas. `auth/signup` continua desabilitado.

A simulação restrita apontou atualização de 2 funções e 10 endpoints, sem tabelas ou registros. O usuário autorizou e os 12 contratos foram publicados, com a exportação remota conferida. As tarefas 4.2 e 4.3 ainda dependem das requisições negativas autenticadas e dos fluxos reais, respectivamente. A verificação visual de 3.4 permanece pendente porque a sessão não disponibilizou navegador. Resultados, contratos e saída da simulação estão documentados em `docs/portal-gerencial.md`. Nenhuma pendência foi considerada concluída por presunção.
