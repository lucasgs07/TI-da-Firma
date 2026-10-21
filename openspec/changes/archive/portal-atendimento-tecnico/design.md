# Design

## Context

Ver `proposal.md` para a motivação. A interface atual direciona apenas o perfil 4 ao portal de chamados. O cliente HTTP já consulta lista e detalhe, mas ainda não integra as ações técnicas. Os arquivos exportados possuem associação múltipla em `chamado_tecnico`, comentários em `interacao_chamado` e operações de atendimento com autoria derivada da sessão.

As consultas de lista/detalhe e interações aplicam filtros técnicos de aberto ou associação; `require_ticket_read` é ainda mais restritivo para chamados abertos atribuídos a outra pessoa. A nova política exige alinhar esses pontos e `get_actor_scope`. A documentação conceitual contém decisões antigas sobre frontend; prevalece a arquitetura Reflex/Xano já adotada. Não há evidência aqui de equivalência entre arquivos locais e ambiente remoto.

## Goals / Non-Goals

**Goals:** manter autorização no Xano, reutilizar contratos existentes e separar leitura global de escrita por associação; preservar a área do funcionário.

**Non-Goals:** integração com GLPI, reprodução completa de suas telas, novas tabelas, alterações em ativos/tarefas/indicadores ou permissões administrativas.

## Decisions

1. **Área técnica após validação da sessão.** Renderizar lista e detalhe próprios para perfil 3 usando o fluxo de login existente; validar o perfil também nos eventos. Separar componentes/estado de atendimento quando necessário para não ampliar as verificações exclusivas do funcionário. Alternativa rejeitada: liberar a tela do funcionário para todos, pois ela tem contrato exclusivo e não contém operações técnicas.
2. **Leitura global explícita no backend.** Ajustar `get_actor_scope`, `require_ticket_read`, GET `/chamado`, GET `/chamado/{id}` e consultas de interações para permitir ao técnico qualquer chamado existente. Preservar escopos dos demais perfis e listas explícitas de campos públicos. Leitura nunca deve ser usada como autorização implícita para PATCH/POST. Revisar consumidores dos helpers para evitar ampliação indireta de escrita.
3. **Detalhe inspirado na organização funcional solicitada.** Cabeçalho com número, título e status; painel de contexto com solicitante, categoria, prioridade e técnicos; área principal com descrição, histórico cronológico e comentários; ações de associação/status/solução. Responsividade e identificação clara de ações indisponíveis. Não depende de consulta ou integração externa com GLPI.
4. **Contratos reaproveitados.** GET `/chamado` e `/chamado/{id}` mantêm lista/objeto e nomes públicos existentes, incluindo `requester_name`, `tecnicos`, `status_name`. GET `/interacao_chamado` ganha filtro opcional `chamado_id`, aplicado no backend e preservando compatibilidade sem filtro; retornar `id`, `chamado_id`, `user_id`, `mensagem`, `created_at` e nome público do autor por projeção segura. Revisar também GET individual de interação para a mesma política. Não baixar todos os comentários para filtrá-los apenas na interface.
5. **Escrita conservadora.** POST `/chamado/{id}/assumir` continua permitindo apenas `Aberto`, associa o ator autenticado e preserva outros técnicos, com repetição idempotente. `chamado_tecnico` prevalece; usar `responsavel_id` legado apenas quando não houver associações. POST `/interacao_chamado` mantém autoria pelo servidor e permissão do técnico associado; o contrato atual permite comentários mesmo após conclusão e isso é preservado. PATCH `/chamado/{id}` mantém `status_nome` e `solucao_final`, exige associação e bloqueia mudanças operacionais em resolvidos/fechados. Alternativa rejeitada: permitir escrita global porque a leitura é global.
6. **Status existentes.** A interface apresenta `Em atendimento` como ação de iniciar atendimento, sem criar o estado `Em andamento`. Os nomes suportados são os já aceitos no endpoint; IDs nunca são presumidos. Configuração ausente deve gerar erro claro, sem criar cadastros automaticamente. Resolver ou fechar exige solução não vazia na mesma requisição. Não adicionar reabertura nem mudança automática de status ao assumir.
7. **Atualização e erros.** Após sucesso, recarregar detalhe, associações, histórico e lista pertinentes; durante envio bloquear repetição. Em falha, preservar texto editado e não antecipar sucesso; em sessão expirada limpar dados e retornar ao login. Troca de chamado/logout limpa rascunhos e dados anteriores. Falha de histórico deve ser distinguida de histórico vazio.

## Risks / Trade-offs

- Leitura global expõe conteúdo de todos os chamados aos técnicos → decisão explicitamente confirmada; manter projeções seguras e testes entre perfis.
- Helpers com regras divergentes → cobrir lista, detalhe e interações com a mesma matriz de leitura, sem alterar guardas de escrita.
- Estado remoto divergente → comparar contratos e exportações antes da integração; arquivos locais não comprovam publicação.
- Concorrência entre associação e conclusão → backend deve revalidar elegibilidade ao gravar; cobrir chamadas concorrentes e não confiar no estado mostrado no navegador.
- Consulta global sem paginação existente pode crescer → evitar consultas globais de comentários; paginação geral fica fora desta mudança e deve ser avaliada separadamente se o volume exigir.

## Migration Plan

1. Alterar e validar contratos locais e testes de autorização, mantendo representações em `apis/`, `functions/` e `database/xano-export/` coerentes.
2. Executar simulação das mudanças remotas, apresentar impacto e aguardar autorização explícita antes de publicar no Xano.
3. Verificar backend autorizado e então integrar/validar o portal Reflex. Confirmar fluxo completo com técnico e regressão de funcionário.
4. Em reversão, desabilitar a área técnica e restaurar somente as mudanças desta entrega por revisão de diff; não excluir dados, associações ou comentários. Reversão remota também exige simulação e autorização.
