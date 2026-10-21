# Design

## Context

Ver `proposal.md`. O frontend em `TI_da_Firma.py` já seleciona portais para perfis 2/3/4; o perfil 1 usa conteúdo genérico. `OfficeState` restringe eventos a gestores e trabalhadores, portanto não basta reutilizar essa tela alterando o perfil local.

As exportações confirmam `chamado`, `interacao_chamado`, `tarefa`, `user`, `perfil`, `departamento` e `status_chamado`. Leitura global do administrador já existe nas consultas e em `task_access`. `users/create` aceita perfis 1–4 e valida técnico em T.I. A métrica `helpdesk/metrics/technicians` mede atribuições por técnico e não representa o total de chamados. `logs/events`, de outro grupo de API (canonical `qMqoH8ER`), retorna eventos genéricos sem metadados. Não foi encontrada nos endpoints de chamados uma trilha completa de alterações em `event_log`.

## Goals / Non-Goals

**Goals:** Reutilizar autorização e dados existentes, calcular indicadores no Xano e servir histórico paginado com projeção pública. Implementar o frontend com Reflex, seguindo suas skills na fase apply.

**Non-Goals:** Novas tabelas, auditoria retroativa, logs técnicos do servidor, metadados arbitrários, edição de chamados/tarefas, criação de tarefas pelo portal, gestão de ativos, gráficos adicionais ou alteração da regra de departamento do técnico. Permissões legadas de escrita do administrador no backend não serão removidas nesta mudança: o modo consulta descreve a nova interface, sem quebra dos contratos existentes.

## Decisions

1. **Estado administrativo dedicado.** Criar componentes e estado próprios; compartilhar transformações públicas e transporte HTTP onde seguro, sem estender indiscriminadamente eventos de `OfficeState`. Validar sessão por `auth/me`, proteger eventos e limpar estado na troca de sessão. Alternativa de ampliar todo o estado gerencial aumenta risco de liberar ações fora do escopo.

2. **Indicadores agregados globais.** Propor GET `helpdesk/metrics/tickets` no grupo Authentication, protegido por `require_admin`. Resposta: `abertos`, `em_andamento`, `finalizados`, `nao_classificados` e `total`, inteiros não negativos. Contar diretamente `chamado`, agrupado por nomes de status existentes; não juntar responsáveis para contagem. A soma dos quatro grupos deve corresponder ao total da mesma leitura lógica. Não calcular a partir da página visível nem somar a métrica dos técnicos. Status novos não exigem inventar IDs: entram em não classificados.

3. **Consultas existentes preservadas.** Usar GET `chamado`, GET `chamado/{id}`, GET `tarefa` e GET `tarefa/{id}` para consulta administrativa, com projeções públicas. Confirmar campos de nomes do solicitante/responsáveis e adicionar projeções seguras quando ausentes, sem recorrer a diretório irrestrito. Preservar `responsaveis_ids` como fonte canônica e fallback em `responsavel_id`. Não mudar unilateralmente respostas de listas usadas pelos outros portais; eventual paginação compartilhada deve ser opcional e manter compatibilidade. Listas hoje sem paginação podem permanecer assim no MVP, com carregamento/erro explícitos; o histórico novo será paginado.

4. **Logs significam interações registradas.** Propor GET `helpdesk/tickets/history` no grupo Authentication, exclusivo do administrador. Entradas: `chamado_id` opcional positivo, `page` padrão 1 e `per_page` padrão 100, limitado a 100. Resposta paginada com `items`, `nextPage`, `itemsTotal` e `pageTotal`; linhas com `id`, `chamado_id`, `created_at`, `user_id`, `author_name`, `mensagem`. Ordenar por data e ID ascendentes; validar chamado inexistente quando filtro informado e aceitar histórico vazio de chamado existente. Reutilizar tabela e autorização de interações; não alterar os contratos dos logs genéricos. A data privada no schema já é projetada explicitamente pelo endpoint atual de interações: aplicar whitelist igualmente. Autor ausente mantém ID e nome indisponível.

5. **Download CSV a partir de páginas autorizadas.** Consultar todas as páginas de `helpdesk/tickets/history` no backend Reflex, com token fora de URLs. Usar o mesmo filtro da tela, deduplicar por ID e detectar ciclos de paginação. Capturar no início um limite superior de ID do escopo e retornar esse limite na primeira resposta (`through_id`); as páginas seguintes devem enviá-lo para excluir novas interações durante o download. O endpoint deve validar inteiro positivo, sem aceitar ampliação além do limite da primeira página no cliente. Isso fixa o conjunto de interações novas, sem prometer snapshot transacional de nomes alterados durante a leitura. Não gravar arquivo em pasta pública: gerar conteúdo somente para a sessão e liberar temporários em sucesso, erro e logout. CSV UTF-8 com BOM, colunas fixas da spec, serialização padrão e neutralização de campos textuais com prefixos de fórmula (`=`, `+`, `-`, `@`, tabulação/retorno, incluindo após espaços). Concluir todas as páginas antes de oferecer o arquivo. A alternativa de baixar somente a página visível não atende ao escopo; usar o grupo genérico de logs criaria dependência e semântica incorretas.

6. **Cadastro reutilizado.** Chamar `users/create`, `perfil` e `departamento` existentes; apresentar os quatro perfis e departamento obrigatório no formulário, fixando técnico ao departamento T.I. já usado (ID 1). Manter a validação no Xano e não persistir senha em armazenamento local. Confirmar a referência de T.I. no ambiente alvo antes da publicação, sem renumerar ou migrar usuários.

## Risks / Trade-offs

- [Histórico incompleto como auditoria] → Nomear a seção como histórico registrado e documentar que mudanças não registradas não serão reconstruídas.
- [Volume de downloads] → Paginação de 100, progresso e controle de erro; geração em memória tem custo proporcional ao arquivo. Nunca cortar silenciosamente; reavaliar streaming se o volume real impedir a geração.
- [Alterações durante leitura] → Limite superior por ID fixa novas inserções; nomes podem refletir consulta atual, e isso não é exportação transacional de auditoria.
- [Dados sensíveis no estado/CSV] → Whitelists, testes negativos por perfil, token só no transporte autenticado, temporários por sessão e neutralização de fórmulas.
- [Regressões nos portais existentes] → Preservar formatos e permissões compartilhadas; testar os quatro perfis.

## Migration Plan

1. Implementar contratos e testes locais, mantendo pares fonte/exportação e sem alterar schema.
2. Comparar contratos remotos, executar push restrito com `--dry-run`, apresentar impacto e obter autorização explícita antes de publicar.
3. Publicar somente arquivos aprovados, obter nova exportação sem registros/variáveis e conferir consistência.
4. Executar testes Xano de autorização/agregação/histórico e testes do frontend, compilar Reflex e validar desktop/celular e CSV real.
5. Rollback: reverter os contratos desta mudança e a entrada administrativa preservando os portais existentes; não apagar dados ou tabelas. Não remover endpoint novo já utilizado sem avaliar consumidores.
