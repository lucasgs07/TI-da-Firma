# Design

## Context

Ver `proposal.md` para a motivação. A exportação contém `user.name`, `email` único, `password` do tipo password, `perfil_id`, `departamento_id` e `status` com padrão Ativo. Não existem campos de entrega de credenciais ou obrigação de troca. `users/directory` já é paginado e seguro, mas omite e-mail. `users/create` recebe senha manual; o endpoint de boas-vindas envia apenas texto genérico. Login e contexto do ator não verificam status. A listagem de chamados já retorna IDs de prioridade/status e nome do solicitante, sem filtros de entrada. Os filtros locais do Reflex são incompletos entre perfis. Recuperação de senha está fora do escopo desta mudança; os endpoints legados não serão corrigidos nem apresentados como funcionalidade concluída.

## Goals / Non-Goals

**Goals:** reaproveitar tabelas e autorização Xano, separar leitura administrativa de seletores gerenciais e produzir contratos testáveis de filtros e provisionamento.

**Non-Goals:** migrar senhas antigas, permitir edição por gestores, apagar usuários, editar chamados como admin, introduzir tabelas de fila, implementar recuperação/redefinição de senha ou exigir troca de senha no primeiro acesso.

## Decisions

1. **Diretório e edição administrativos.** Reutilizar `GET users/directory` para paginação global de admin, sem restringir perfil/departamento por padrão. Acrescentar e-mail somente à projeção administrativa, preservando seletores gerenciais. Propor `GET users/{user_id}` e `PATCH users/{user_id}` exclusivos de admin. Aceitar apenas `name`, `email`, `perfil_id`, `departamento_id`, `status`; rejeitar campos desconhecidos, senha, hash, tokens e mudança de ID. Validar e-mail único excluindo o próprio registro, referências existentes e técnico exclusivamente em T.I. Não reatribuir chamados ou tarefas ao editar perfil/departamento. Alternativa descartada: liberar PATCH genérico da tabela, que expõe campos e contorna permissões.

2. **Status com efeito real.** Ativo/Inativo deve ser verificado no login, `auth/me` e helper central de contexto a cada requisição protegida. Contas antigas com status nulo/vazio preservam acesso legado até normalização explicitamente revisada; Inativo bloqueia sempre. Mudanças de perfil/departamento usam o registro atual, não extras do token. Rejeitar inativação ou remoção do perfil do último admin ativo, com garantia contra concorrência, para evitar perda total de administração; esse é um controle de integridade proposto nesta mudança. Não prometer revogação criptográfica dos tokens: negar seu uso operacional após inativação é suficiente.

3. **Filtros no backend.** Adicionar parâmetros opcionais `prioridade_id`, `status_chamado_id`, `solicitante_nome` ao GET de chamados, mantendo retorno em lista para compatibilidade. Aplicar `(escopo do ator) AND (filtros)`, com agrupamento explícito dos ORs de escopo. Nome com correspondência parcial, sem distinguir maiúsculas/minúsculas, trim e limite de 200 caracteres; prioridade/status por IDs existentes. Ausência significa sem filtro; ID inválido gera erro de entrada. Reutilizar busca por número/título atual como refinamento local sobre os resultados autorizados, sem removê-la. Não criar índice/tabela sem avaliação do esquema. Todos os portais têm Aplicar/Limpar; vazio e erro são distintos. Funcionário pode pesquisar nome, mas continua vendo só seus chamados. Alternativa descartada: carregar diretório global para selecionar solicitantes.

4. **Preservar senha manual.** Manter o campo de senha nos formulários e no contrato autenticado `users/create`. Administradores e gestores continuam definindo a senha inicial, validada pelas regras existentes (mínimo de oito caracteres, uma letra e um número). Não impor sufixo nem formato numérico, não gerar credencial e não enviá-la por e-mail. Preservar somente o hash no Xano, limpar o campo após envio e nunca registrar senha ou token em respostas, logs ou armazenamento persistente. A edição cadastral continua sem alterar senha.

## Risks / Trade-offs

- [Mudança de perfil/departamento afeta escopos] → reavaliar backend em cada chamada, preservar relações e testar tarefas compartilhadas/legadas e consultas departamentais.
- [Proteção do último admin em concorrência] → validar dentro de mecanismo transacional/serialização suportado pelo Xano; não depender de contagem isolada seguida de atualização.
- [Exports locais não comprovam remoto] → simulação, aprovação e verificação remota antes de declarar conclusão.

## Migration Plan

1. Implementar e testar localmente contratos e projeções, mantendo fontes/exportação consistentes. Não alterar estrutura da tabela user para esta entrega.
2. Preservar `users/create` e seus consumidores com senha manual; manter os endpoints e fluxos legados de recuperação fora desta alteração.
3. Verificar listagem completa, edição validada, bloqueio de contas inativas, proteção concorrente do último administrador e filtros nos quatro perfis, preservando associações e permissões.
4. Executar `xano workspace push --dry-run` restrito ao escopo, apresentar saída e aguardar autorização explícita. Só então publicar e verificar endpoints e exportações.
5. Compilar Reflex e executar testes dos quatro perfis. Rollback deve desativar a funcionalidade nova e restaurar contratos coordenadamente; nunca redefinir senhas ou excluir usuários já criados para reverter código.

## Open Questions

- Confirmar no ambiente alvo o mecanismo de serialização das edições administrativas e um ambiente autorizado para testes concorrentes. Não substituir o bloqueio transacional por uma contagem vulnerável a concorrência.
