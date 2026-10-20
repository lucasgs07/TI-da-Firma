# Tasks

## Validação manual confirmada — 20/10/2026

O usuário informou que realizou todos os testes manuais sugeridos e que tudo funcionou: dashboard, consulta de chamados/tarefas de departamentos diferentes, cadastro dos quatro perfis com técnico em T.I., logs globais/filtrados, download CSV, troca de sessão e visualização no celular. A lista sugerida incluía CSV com mais de 100 interações quando disponível; o relato não informa o volume efetivamente testado. Evidência relatada pelo usuário, sem observação direta pelo agente.

A validação visual do item 3.4 foi concluída com esse relato e a compilação já verificada. Os fluxos positivos de 4.4 foram validados manualmente, mas suas requisições negativas diretas e o volume do CSV não foram individualmente documentados. Os quatro testes automatizados dos endpoints continuam com o resultado HTTP 401 registrado; o sucesso manual não os transforma em testes automatizados aprovados. Os demais critérios específicos ainda abertos permanecem identificados no checklist.

## Publicação — 20/10/2026

Resultado final da função alterada: cinco testes com mocks passaram no Xano, após corrigir o campo ausente. Isso não comprova os endpoints autenticados nem a consulta real do solicitante, já que os mocks usam solicitante nulo.

Simulação autorizada explicitamente pelo usuário; três contratos publicados no workspace 147362/v1 e exportação final conferida. A função recebeu uma correção nos mocks legados: `solicitante_id: null`, necessária à nova projeção do solicitante; foi simulada e publicada sem alterar regras de negócio. Os quatro testes dos endpoints foram tentados, mas retornaram HTTP 401 antes das asserções; permanecem sem aprovação. A autenticação dos endpoints foi preservada. Os registros locais abaixo são históricos; 4.2 está concluído, enquanto 4.3 continua aberto por depender das validações autenticadas dos endpoints. Não foram criados usuários, tarefas ou chamados reais nesta conferência.

## Evidências locais — 20/10/2026

Implementação local do portal, cliente, exportação e contratos preparada. **141 testes Python passaram** (`pytest tests -q -p no:cacheprovider`), incluindo 36 casos novos do administrador. `reflex compile --dry` passou após a última alteração. Os três pares fonte/exportação são idênticos. Cadastro e consultas existentes foram comparados com nova exportação remota e correspondem às fontes; o helper só acrescenta projeção do solicitante. A simulação restrita retornou uma função atualizada e dois endpoints criados, sem schema ou registros; ainda não houve publicação.

Os itens 1.1–1.4 continuam abertos porque seus testes reais Xano ainda não foram executados. Há quatro testes com mocks nos endpoints novos; não foram executados no serviço e não substituem filtros/autorização reais. A compilação de 3.4 passou, mas a verificação visual permanece pendente. 4.2 aguarda autorização da simulação apresentada; 4.3–4.5 dependem da publicação, validação real e encerramento. Consulte `docs/portal-admin.md` para contratos, impacto e limitações. Não há alteração de schema nem alegação de testes remotos executados.

## 1. Contratos e autorização Xano

- [ ] 1.1 Implementar GET `helpdesk/metrics/tickets` com `require_admin` e contrato do design; testar seis status, desconhecidos, vazio, chamados sem técnico ou com vários técnicos, soma dos grupos e negação aos outros perfis.
- [ ] 1.2 Implementar GET `helpdesk/tickets/history` com whitelist, filtro opcional de chamado, paginação e limite superior `through_id`; testar ordem data/ID, páginas adicionais, novos eventos durante leitura, filtro inválido/inexistente, histórico vazio, autor ausente e negação a não administradores.
- [ ] 1.3 Conferir leitura global de chamados e tarefas pelos contratos existentes e completar somente projeções públicas necessárias ao detalhe; testar outro departamento, finalizados, múltiplos responsáveis, fallback legado e compatibilidade dos consumidores existentes.
- [ ] 1.4 Validar `users/create` e referências de T.I., perfil e departamento para os quatro perfis pelo administrador; testar técnico fora de T.I., e-mail duplicado, senha inválida, perfil/departamento adulterado e ausência de segredos nas respostas, preservando regras dos gestores.
- [x] 1.5 Manter fontes e exportações dos contratos afetados coerentes; conferir diff sem novas tabelas/colunas, exclusões ou credenciais e documentar os payloads efetivamente testados.

## 2. Cliente HTTP e estado administrativo

- [x] 2.1 Acrescentar cliente para métricas e histórico paginado e reutilizar consultas/cadastro existentes; testar caminhos, métodos, parâmetros, token no cabeçalho e erros de transporte/autorização sem logs secretos.
- [x] 2.2 Criar estado administrativo com inicialização após sessão validada, seções e loading/vazio/erro; testar login/restauração de administrador, perfil local adulterado, logout, troca de usuário e limpeza de dados administrativos.
- [x] 2.3 Implementar consulta global e detalhe de chamados/tarefas em modo leitura; testar registros externos ao departamento, todos os associados, registros legados e ausência de chamadas de mutação ao navegar.
- [x] 2.4 Implementar cadastro dos quatro perfis com departamento e técnico fixo em T.I.; testar envio duplo, erro preservando dados não secretos, limpeza de senha, rejeição de sessão e confirmação somente após sucesso.
- [x] 2.5 Implementar exportação CSV completa do filtro selecionado, respeitando `through_id`, deduplicação e detecção de ciclos; testar múltiplas páginas, novas inserções, acentos/aspas/quebras, prefixos de fórmula, vazio com cabeçalho, falha intermediária e descarte ao trocar sessão sem arquivo parcial ou público.

## 3. Interface Reflex

- [x] 3.1 Criar entrada exclusiva do perfil 1 e Dashboard com três contadores, total/não classificados quando aplicável e recarga; verificar renderização de zero, loading e erro sem números fabricados.
- [x] 3.2 Criar seções separadas Chamados e Tarefas com lista/detalhe e nomes públicos; verificar navegação completa, solução/conclusão e ausência de botões de atendimento, atribuição, comentário, criação ou exclusão desses registros.
- [x] 3.3 Criar formulário Usuários e seção Logs com consulta global/individual, paginação e download CSV; testar sincronização do filtro exportado, bloqueio durante exportação, histórico vazio e mensagens de falha.
- [x] 3.4 Compilar com `reflex compile --dry` conforme a skill de processos e validar visualmente desktop/celular; registrar resultados e regressão dos demais portais sem marcar verificações não executadas como concluídas.

## 4. Integração e publicação

- [x] 4.1 Executar regressões Python de autenticação e portais técnico/gerencial/funcionário, além dos testes administrativos; registrar quantidade e resultados reais e revisar arquivos sem credenciais.
- [x] 4.2 Comparar contratos locais e remotos e executar push restrito com `--dry-run`; apresentar saída e impacto, obtendo autorização explícita antes de qualquer alteração remota, sem opções destrutivas.
- [ ] 4.3 Após autorização, publicar somente contratos aprovados, obter exportação sem registros/variáveis e conferir correspondência; executar testes Xano de autorização, métricas e histórico, registrando evidências.
- [ ] 4.4 Validar fluxos reais de administrador: dashboard confrontado com dados, chamados/tarefas globais, cadastro dos quatro perfis e CSV com mais de uma página; executar requisições negativas dos demais perfis e registrar ausência de vazamento entre sessões.
- [ ] 4.5 Atualizar documentação operacional e checklist com evidências, distinguindo testes automatizados e confirmação manual; sincronizar especificação e arquivar somente após concluir os critérios do escopo.
