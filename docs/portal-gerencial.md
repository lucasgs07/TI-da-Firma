# Portal gerencial e tarefas do funcionário

## Encerramento — 20/10/2026

O usuário confirmou também os testes restantes de permissões e entradas inválidas no backend. O checklist foi concluído em 27/27 com essa validação manual relatada, além das evidências automatizadas já registradas. A especificação principal `manager-portal` foi sincronizada com todos os requisitos aprovados. Os registros de pendências abaixo são históricos e foram superados por esta confirmação. O destino do arquivamento é `openspec/changes/archive/2026-10-20-portal-gerencial-por-departamento/`.

## Validação manual — 20/10/2026

O usuário confirmou o funcionamento dos fluxos reais, a visualização em desktop/celular e a conclusão simultânea de uma tarefa por dois responsáveis. A confirmação foi relatada pelo usuário, sem observação direta pelo agente. Os itens 3.4, 4.3 e 4.4 estão concluídos: progresso atualizado para 17/27. Os registros abaixo preservam o histórico das verificações anteriores. Restam os critérios específicos de testes negativos/backend descritos nas tarefas abertas; o arquivamento ainda não foi executado.

## Permissões implementadas localmente

| Usuário | Chamados | Cadastro de usuários | Tarefas |
| --- | --- | --- | --- |
| Gestor T.I. (perfil 2, departamento 1) | Consulta global e abertura própria | Funcionário/gestor em qualquer departamento; técnico sempre T.I.; nunca administrador | Cria para técnicos T.I. |
| Outro gestor (perfil 2) | Consulta dos membros do próprio departamento e abertura própria | Somente funcionário do próprio departamento | Cria para funcionários do próprio departamento |
| Funcionário (perfil 4) | Abertura e consulta próprias, sem atendimento | Não autorizado | Consulta e conclui somente tarefas atribuídas a ele, com solução obrigatória |

A referência de T.I. (`departamento_id` 1) vem das regras preexistentes do projeto. Não se criou tabela, coluna, perfil ou departamento. A confirmação do cadastro efetivo e as validações autenticadas no serviço continuam pendentes antes da entrega completa.

## Interface Reflex

Após `auth/me`, gestores recebem navegação para Chamados, Abrir chamado, Cadastrar usuário e Nova tarefa. O diretório de responsáveis é percorrido por todas as páginas e filtrado pelo perfil/departamento permitido. A lista de chamados gerencial leva a detalhe e histórico somente de consulta.

Técnicos e funcionários possuem navegação entre Chamados (`/`) e Minhas tarefas (`/tarefas`), em telas separadas. Minhas tarefas apresenta somente as atribuídas ao usuário, com detalhe e campo de solução. Concluir tarefa envia apenas `status_nome: Concluída` e `solucao_aplicada` ao PATCH de tarefa. A operação não modifica chamado, mesmo quando existe vínculo. Conclusão e data originais são preservadas em repetição idêntica; solução diferente em tarefa concluída é rejeitada pelo contrato Xano. O suporte ao técnico usa as permissões já publicadas, sem nova alteração remota.

Senha inicial é recebida somente no envio do formulário e não é colocada em variável de estado ou LocalStorage. O campo é limpo após a tentativa; após sucesso, o formulário é remontado. Falhas preservam campos não secretos. Rejeição de sessão limpa o estado e direciona ao login; rejeição de uma operação não encerra uma sessão válida. Logout e nova validação de sessão limpam os dados gerenciais e rascunhos de tarefas.

## Contratos envolvidos

- `get_actor_scope` e `require_ticket_read`: capacidades por departamento e leitura coerente dos membros do departamento, independentemente de perfil.
- GET `/chamado`, `/chamado/{id}` e consultas de interações: mesma matriz de leitura, sem ampliar escrita de chamados.
- POST `/users/create`: gestor T.I. pode criar perfis 2/3/4 com departamentos permitidos; demais gestores somente perfil 4 próprio; técnico novo sempre T.I., inclusive quando criado por administrador.
- GET `/users/directory`: resposta paginada segura; gestor comum limitado a funcionários do próprio departamento. Sem senhas ou tokens.
- POST `/tarefa` e reatribuição em PATCH: alvo técnico T.I. para gestor T.I.; funcionário departamental para demais gestores, com validação no servidor no envio.
- GET de lista/detalhe de tarefas: funcionário vê somente as próprias; gestor acompanha o escopo correspondente a seus responsáveis elegíveis. Nenhum vínculo de tarefa concede leitura de chamado.
- PATCH de tarefa: inclui funcionário responsável no ramo de conclusão já existente, mantendo whitelist, solução obrigatória, status `Concluída` configurado, data do servidor e imutabilidade após conclusão.
- `auth/signup` foi inspecionado e permanece desabilitado. Usuários legados não foram migrados nem excluídos.

## Verificações em 20/10/2026

- 86 testes Python passaram com `python -m pytest tests -q -p no:cacheprovider`, incluindo regressões do funcionário/técnico e 18 casos novos de estado/cliente gerencial.
- `reflex compile --dry` passou.
- Os testes novos verificam seleção departamental, perfis de cadastro, técnico fixo em T.I., limpeza de senha, tarefa alheia, conclusão própria, solução preservada em falha, ausência de atualização de chamados, logout, sessão rejeitada, bloqueio de envio duplo, paginação completa/circular e campos dos contratos de gravação.
- O inventário de navegação desta sessão não contém navegador, portanto a inspeção visual desktop/móvel não foi executada.
- Os testes Python não executam XanoScript. Testes remotos das versões alteradas, tentativas diretas negativas e os fluxos reais ainda precisam ser executados após publicação autorizada.

## Comparação e simulação

Foi obtida uma cópia dos contratos atuais do workspace 147362, branch v1, em pasta temporária, sem `--records` ou `--env`. Os 12 contratos envolvidos foram comparados; não se alterou o remoto. Fontes locais e exportações foram mantidas coerentes; conferência de delimitadores não substitui execução no Xano.

A simulação `xano workspace push --dry-run` restrita aos arquivos desta mudança retornou:

```text
Matched: 12 of 194 files
=== Push Preview: workspace 147362 ===
Functions            ~2 updated
API Endpoints        ~10 updated
UPDATE function helpdesk/access/get_actor_scope
UPDATE function helpdesk/access/require_ticket_read
UPDATE query chamado/{chamado_id} GET
UPDATE query chamado GET
UPDATE query interacao_chamado/{interacao_chamado_id} GET
UPDATE query interacao_chamado GET
UPDATE query tarefa/{tarefa_id} GET
UPDATE query tarefa GET
UPDATE query tarefa POST
UPDATE query tarefa/{tarefa_id} PATCH
UPDATE query users/create POST
UPDATE query users/directory GET
```

Não há tabelas, registros, exclusões ou variáveis de ambiente na seleção. A publicação amplia cadastro pelo gestor T.I., troca a elegibilidade de responsáveis dos demais gestores para funcionários próprios e libera leitura/conclusão de tarefas próprias ao funcionário.

## Publicação autorizada — 20/10/2026

O usuário autorizou explicitamente a simulação acima. O push restrito aos 12 arquivos foi confirmado no prompt interativo, sem opções destrutivas ou `--force`. Resultado: `Pushed 12 documents to workspace 147362 ... in 4.3s`; o CLI sincronizou seis GUIDs locais.

Uma nova exportação foi obtida sem registros ou variáveis de ambiente. Os 12 contratos remotos correspondem ao conteúdo esperado, com diferenças apenas de formatação, e suas fontes/exportações locais foram alinhadas ao formato canônico retornado. Não foram criados usuários, tarefas ou chamados reais durante essa conferência.

Os 20 testes unitários das duas funções publicadas passaram no Xano: cinco de `get_actor_scope` e quinze de `require_ticket_read`, incluindo a leitura de membros de outros perfis do mesmo departamento, negação entre departamentos e regressões dos demais perfis. Esses testes usam mocks; não comprovam as operações de cadastro e tarefas dos endpoints.

## Pendências

Confirmar cadastro T.I.; executar testes Xano das regras alteradas e fluxos reais com gestor T.I., gestor de outro departamento e funcionário; verificar visualmente desktop/móvel. As tarefas que dependem dessas validações permanecem abertas. Não arquivar esta mudança antes de concluir os critérios.

### Preparação do arquivamento

Mudança: `portal-gerencial-por-departamento` (schema `spec-driven`). A conferência em 20/10/2026 retornou 14 de 27 tarefas concluídas; os quatro artefatos de planejamento estão prontos. O arquivamento ainda não foi executado, pois o `AGENTS.md` exige concluir e validar o escopo antes dessa etapa.

Após registrar as evidências das validações pendentes em `tasks.md`, conferir novamente o progresso, comparar a delta `specs/manager-portal/spec.md` com a especificação principal, sincronizar as diferenças pelo fluxo OpenSpec e validar o resultado. Só então arquivar a mudança, preservando seus metadados. A data do diretório de arquivo deve ser a data efetiva da operação.

## Revisão: vários responsáveis por tarefa — publicada

O usuário confirmou que qualquer responsável pode concluir a tarefa inteira, com solução obrigatória. O formulário agora permite marcar um ou mais técnicos de T.I. para o gestor T.I. ou funcionários do próprio departamento para os demais gestores. Os nomes dos associados aparecem na lista/detalhe. A conclusão grava uma única solução e data compartilhadas por todos, sem modificar chamados.

Foi preparado o campo opcional `tarefa.responsaveis_ids`, referência múltipla a `user`. Uma lista preenchida prevalece sobre `responsavel_id`; tarefas antigas sem lista continuam usando seu responsável único. Criação/reatribuição validam todos antes da gravação, removem IDs duplicados e mantêm o primeiro no campo legado para compatibilidade. Não há migração em massa nem exclusão de dados. Clientes anteriores podem enviar `responsavel_id` como alternativa à lista; enviar os dois campos é rejeitado.

O novo helper `helpdesk/access/task_access` é usado nas cinco operações de tarefa para unificar a autorização. Técnicos e funcionários associados podem ler/concluir em qualquer posição da lista. Um gestor só gerencia uma tarefa quando todos os seus responsáveis estão no escopo do gestor; isso também impede contorno pelo endpoint de exclusão. A lista retorna uma tarefa por registro, sem duplicá-la por responsável. A consulta interna percorre tarefas e resolve o acesso individualmente, portanto há custo proporcional ao volume.

Verificação local: **105 testes Python passaram**, e `reflex compile --dry` passou. Os 15 novos casos cobrem associados secundários dos dois perfis, conclusão global, prioridade da lista sobre o campo legado, compatibilidade antiga, seleção múltipla/duplicada/inválida e preservação em erro. Os cinco testes unitários com mocks do helper também passaram no Xano após a publicação. A conferência dos sete pares fonte/exportação passou. Inspeção visual, persistência em fluxos reais e concorrência real seguem pendentes.

Simulação restrita apresentada antes da autorização:

```text
Matched: 7 of 196 files
Tables               ~1 updated
Functions            +1 created
API Endpoints        ~5 updated
UPDATE table tarefa
ADD_FIELD table tarefa
CREATE function helpdesk/access/task_access
UPDATE query tarefa/{tarefa_id} DELETE
UPDATE query tarefa/{tarefa_id} GET
UPDATE query tarefa GET
UPDATE query tarefa POST
UPDATE query tarefa/{tarefa_id} PATCH
```

A seleção foi autorizada explicitamente e publicada: `Pushed 7 documents to workspace 147362 ... in 11.5s`. O CLI sincronizou três GUIDs locais. Uma nova exportação, sem registros ou variáveis de ambiente, confirmou os sete contratos; fontes e exportações locais foram alinhadas à formatação canônica retornada, incluindo a normalização das expressões de `array.has`.

Os cinco testes do helper `helpdesk/access/task_access` passaram no Xano: técnico secundário, funcionário secundário, responsável legado, negação para funcionário não associado e negação para gestor com responsável externo. São testes com mocks; não criaram tarefas ou usuários reais. Permanecem pendentes os fluxos autenticados de criação/conclusão, persistência, concorrência real e verificação visual. A publicação não conclui essas validações.
