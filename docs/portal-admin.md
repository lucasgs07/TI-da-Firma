# Portal administrativo

## Validação manual confirmada — 20/10/2026

O usuário relatou sucesso em todos os testes manuais sugeridos: indicadores, consultas globais e detalhes, cadastro dos quatro perfis, técnico fixo em T.I., logs globais/individuais, CSV, isolamento após logout e visualização no celular. Essa é confirmação manual do usuário, sem observação direta pelo agente. O volume efetivo do CSV não foi informado. O relato valida os fluxos de uso; permanecem registrados separadamente os testes automatizados de endpoints com HTTP 401 e os critérios específicos de backend ainda não comprovados. Nenhum novo teste automatizado foi executado nesta atualização.

## Publicação autorizada — 20/10/2026

Após autorização explícita da simulação, os três contratos foram publicados no workspace 147362, branch v1: `Pushed 3 documents ... in 7.0s`. O CLI sincronizou dois GUIDs. Foram criados `helpdesk/metrics/tickets` e `helpdesk/tickets/history` e atualizada a projeção do solicitante em `task_access`, sem alteração de schema, registros, exclusões ou variáveis de ambiente.

Os quatro testes dos endpoints foram tentados pelo CLI, mas todos retornaram HTTP 401 (`Authentication Required`) antes das asserções. Os mocks de `require_admin` não substituem a autenticação da camada do endpoint. Esses testes não foram aprovados e precisam ser executados com contexto de autenticação no Xano ou substituídos por verificações autenticadas equivalentes. A proteção dos endpoints foi preservada.

Os testes legados da função inicialmente falharam por ausência de `solicitante_id` nos mocks. Foi corrigido somente o conteúdo desses cinco mocks para declarar solicitante nulo; a correção foi simulada e publicada dentro do mesmo escopo autorizado (`Pushed 1 documents ... in 7.9s`). A exportação final dos três contratos foi conferida e fontes/exportações locais foram alinhadas ao formato canônico retornado, sem registros ou variáveis de ambiente.

Após a correção, os cinco testes de `task_access` passaram no Xano (duas asserções por teste). Os 141 testes Python e a compilação Reflex haviam passado na implementação local. Os registros de preparação abaixo descrevem a etapa anterior à publicação. Continuam pendentes a validação autenticada dos endpoints, os fluxos reais, a inspeção visual e o download real do CSV; não arquivar a mudança por presunção.

## Escopo implementado localmente

O perfil Administrador (1), validado em `auth/me`, recebe Dashboard, Chamados, Tarefas, Usuários e Logs na home Reflex. As consultas globais de chamados e tarefas reutilizam contratos existentes. A interface não oferece criação, atendimento, comentários, atribuição, conclusão ou exclusão de chamados/tarefas. Permissões legadas do administrador no backend não foram revogadas.

O cadastro usa `users/create`: perfis 1–4, departamento existente selecionável e técnicos novos obrigatoriamente em T.I. (referência existente ID 1). A senha só é enviada na submissão, não integra estado persistido e o campo é limpo após a tentativa. Falhas preservam os demais campos; sucesso reinicializa o formulário. A validação de perfil/departamento, e-mail único e senha continua no Xano.

## Contratos novos

- GET `helpdesk/metrics/tickets`: exclusivo do administrador; retorna `abertos`, `em_andamento`, `finalizados`, `nao_classificados` e `total`. Conta cada chamado uma vez, independentemente das atribuições. `Aberto` alimenta abertos; `Em Análise`, `Em atendimento` e `Aguardando usuário` alimentam andamento; `Resolvido`/`Fechado` alimentam finalizados. Qualquer outro status, inclusive ausente, fica em não classificados. O cliente rejeita números negativos ou totais inconsistentes e não mostra zero em caso de erro.
- GET `helpdesk/tickets/history`: exclusivo do administrador; aceita `chamado_id` opcional positivo, `page` a partir de 1, `per_page` até 100 e `through_id` opcional não negativo. Retorna página de `items` públicos, dados de paginação e `through_id`. O filtro é aplicado antes da paginação, com ordem crescente por data/ID. `through_id=0` representa conjunto vazio. A primeira página fixa o maior ID; páginas posteriores reenviam o mesmo limite. O cliente rejeita filtro ignorado, limite alterado ou IDs acima do limite.

O histórico contém somente interações efetivamente salvas em `interacao_chamado`. Não reconstrói alterações antigas nem lê metadados genéricos de `event_log`. Os logs gerais existentes pertencem a outro grupo de API e não são necessários para esta tela.

## Download

Baixar histórico CSV usa o filtro aplicado da tela, independentemente do texto ainda não submetido no formulário. A exportação começa uma leitura completa própria com limite de ID fixo e percorre todas as páginas, removendo duplicações por ID e detectando paginação inválida ou quantidade incompleta. Falha em qualquer página impede o download parcial. Novas inserções após o início não entram; nomes de autores refletem o momento da consulta e não constituem snapshot transacional.

O CSV UTF-8 com BOM contém somente `id`, `chamado_id`, `created_at`, `user_id`, `author_name`, `mensagem`. Campos textuais com prefixos interpretáveis como fórmula são neutralizados; aspas, separadores e quebras usam serialização CSV padrão. Conjunto vazio produz cabeçalho. O conteúdo existe apenas em variáveis locais da chamada e é enviado com `rx.download(data=...)`; não há arquivo em assets, pasta pública ou variável sincronizada. Token segue somente no cabeçalho autenticado. Logout, restauração e rejeição de sessão limpam o estado administrativo. Downloads já salvos pelo usuário não são removidos pelo logout.

## Verificação e publicação

Compilação Reflex e regressões locais estão registradas em `openspec/changes/portal-administrativo/tasks.md`. Os dois endpoints contêm quatro testes Xano com mocks, ainda não executados no serviço. Os testes existentes de `task_access` devem ser reexecutados após sua alteração de projeção (`requester_name`). Mocks não comprovam os filtros reais do banco nem as permissões reais de cadastro; essas validações permanecem pendentes.

Conferência remota sem registros/variáveis: os contratos existentes de cadastro e leitura de chamados/tarefas correspondem às fontes locais. O diff do helper acrescenta somente nome público do solicitante, sem alterar a política de acesso. Os dois endpoints são novos. Fontes e exportações locais afetadas são mantidas em pares.

Simulação restrita, sem publicação:

```text
Matched: 3 of 200 files
Functions            ~1 updated
API Endpoints        +2 created
UPDATE function helpdesk/access/task_access
CREATE query helpdesk/metrics/tickets GET
CREATE query helpdesk/tickets/history GET
```

Nenhuma tabela, coluna, registro, variável de ambiente ou exclusão está selecionada. A publicação depende de autorização explícita desta simulação. Antes dela, os indicadores e a seção de logs novos não estão integrados ao backend remoto. Depois de publicar, conferir nova exportação e executar testes Xano e fluxos reais de administrador e negações dos demais perfis; verificar a interface em desktop/celular e um CSV com múltiplas páginas. Não arquivar enquanto essas verificações estiverem pendentes.

Limitações do MVP: listas compartilhadas continuam completas em memória; métricas fazem uma leitura dos chamados e contagem no Xano, e o CSV ocupa memória proporcional ao volume. Não há truncamento automático. Se o volume inviabilizar o uso, será necessário planejar agregação otimizada/streaming preservando o contrato.

## Gestão de usuários e filtros — mudança em andamento

A implementação local da área Usuários contém lista paginada, total de registros, atualização e abertura do formulário de edição. Perfil e departamento usam os cadastros existentes; técnico permanece vinculado a T.I. O admin pode salvar nome, e-mail, perfil, departamento e Ativo/Inativo. Senha e ID não são campos editáveis. Administrador pode permanecer sem departamento; os demais perfis exigem departamento válido. A proteção do último admin ativo depende de validação concorrente no Xano.

O botão Cadastrar usuário preserva o formulário com senha manual. Não há geração automática, sufixo fixo, envio de senha por e-mail ou recuperação de senha nesta mudança. Após uma edição confirmada, a lista é recarregada; se apenas a atualização da lista falhar, a mensagem informa que a alteração já foi salva. E-mail duplicado ou rejeição do backend mantém o formulário aberto. Logout e sessão rejeitada limpam lista/detalhe.

Na lista de chamados, selecionar prioridade e status, informar parte do nome do solicitante e usar Aplicar filtros. Limpar remove todos os filtros e consulta novamente. Número/título refinam os registros retornados. Filtros não permitem atendimento no portal administrativo.

Esses controles dependem dos contratos novos de usuários e filtros ainda não publicados. Testes Python usam transporte/estado simulados; não comprovam gravação ou autorização remotas. Ver `gestao-usuarios-implementacao.md` para evidências e pendências.
