# Portal de atendimento técnico

## Uso no Reflex

Após login ou restauração da sessão validada por `auth/me`, o perfil 3 recebe a área **Todos os chamados**. O perfil 4 continua no portal exclusivo do funcionário. A tela técnica reúne solicitante, classificação, técnicos associados, descrição, solução e histórico cronológico com identificação do autor e horário com fuso explícito.

- **Associar a mim:** disponível para chamado `Aberto` ao qual o técnico ainda não está associado. Preserva os demais técnicos.
- **Enviar comentário:** disponível ao técnico associado, inclusive após conclusão, conforme contrato existente.
- **Salvar atendimento:** disponível ao técnico associado enquanto o chamado não estiver resolvido/fechado. `Em atendimento` representa o início do atendimento; não foi criado um status `Em andamento`.
- **Resolver/fechar:** exige solução final; não há reabertura nesta entrega.

As verificações da interface servem de orientação. A autorização efetiva permanece no Xano, com identidade derivada do token. As associações retornadas por `tecnicos` prevalecem; o cliente aceita `responsavel_id` como compatibilidade apenas quando a resposta não contém `tecnicos`.

## Contratos

| Operação | Método e caminho | Entrada |
| --- | --- | --- |
| Lista global técnica | GET `/chamado` | Sessão autenticada |
| Detalhe | GET `/chamado/{id}` | ID positivo |
| Histórico | GET `/interacao_chamado?chamado_id={id}` | Filtro opcional, aplicado no servidor |
| Interação individual | GET `/interacao_chamado/{id}` | ID positivo |
| Autoassociação | POST `/chamado/{id}/assumir` | Nenhum ID de usuário no corpo |
| Comentário | POST `/interacao_chamado` | `chamado_id`, `mensagem` |
| Operação | PATCH `/chamado/{id}` | `status_nome`, `solucao_final` quando preenchida; obrigatória para resolver/fechar |

O histórico mantém os campos públicos existentes e acrescenta `author_name`. A ausência do filtro preserva a consulta anterior com o escopo de cada perfil. O cliente técnico rejeita uma resposta que contenha interações de outro chamado, para não expor dados se um servidor antigo ignorar o filtro.

| Perfil | Leitura de chamados | Escrita técnica |
| --- | --- | --- |
| Técnico (3) | Todos, inclusive de outros técnicos e concluídos | Autoassociação em aberto; comentários/status conforme associação e estado |
| Funcionário (4) | Somente próprios | Mantidas as permissões existentes |
| Gestor (2) | Escopo existente por departamento/exceção TI | Sem ampliação |
| Administrador (1) | Escopo existente | Sem ampliação |

Em operações técnicas, HTTP 401 invalida a sessão; 400/403/404/409/422 informa erro da operação sem apagar a sessão. O texto editado é preservado quando o envio falha; não se mostra sucesso sem resposta positiva. Falha ao recarregar após uma gravação confirmada é indicada separadamente. Logout, nova validação de sessão e troca de chamado limpam dados anteriores.

## Verificação local em 20/10/2026

- `.venv/Scripts/python.exe -m pytest tests -q -p no:cacheprovider`: **68 testes passaram**, incluindo regressões do funcionário, contratos HTTP e fluxo técnico integrado com persistência simulada.
- `.venv/Scripts/reflex.exe compile --dry`: compilação concluída com sucesso.
- A verificação visual desktop/móvel não foi executada: o inventário do controle de navegador desta sessão não disponibilizou navegadores.
- Os testes Python simulam o Xano; não comprovam execução de XanoScript nem persistência no serviço remoto. A execução posterior dos testes das funções publicadas está registrada abaixo.

## Comparação e simulação remota

Foi obtida uma cópia de contratos do workspace `147362`, branch `v1`, em diretório temporário, sem `--records` ou `--env`. Os seis contratos existentes correspondem à base local anterior; nas quatro APIs, a exportação acrescenta somente o metadado `guid`. Não houve gravação no workspace remoto.

A simulação com `xano workspace push --dry-run`, restrita aos seis arquivos desta entrega, retornou:

```text
Matched: 6 of 194 files
=== Push Preview: workspace 147362 ===
Functions            ~2 updated
API Endpoints        ~4 updated
UPDATE function helpdesk/access/get_actor_scope
UPDATE function helpdesk/access/require_ticket_read
UPDATE query chamado/{chamado_id} GET
UPDATE query chamado GET
UPDATE query interacao_chamado/{interacao_chamado_id} GET
UPDATE query interacao_chamado GET
```

Não há tabelas, registros, variáveis de ambiente ou exclusões na seleção. A publicação amplia a leitura dos técnicos para todos os chamados e seus comentários.

## Publicação autorizada em 20/10/2026

Após a autorização explícita do usuário, o comando de push restrito aos seis arquivos acima foi confirmado no prompt interativo, sem `--force`, `--delete`, `--sync`, `--records` ou `--env`. Resultado do CLI: `Pushed 6 documents to workspace 147362 ... in 2.9s` e `Synced 6 GUIDs to local files`.

Uma nova exportação remota foi obtida após a publicação. Os seis contratos foram conferidos e suas representações locais em `apis/`, `functions/` e `database/xano-export/` foram alinhadas ao formato canônico retornado pelo Xano (normalização de espaços e separadores de objetos). Não houve alteração de tabelas ou registros de negócio.

Os endpoints não possuem testes unitários cadastrados no Xano (`unit_test list --obj-type query`: `No unit tests found`). A sessão não dispõe de credenciais de usuário técnico para executar o fluxo autenticado real. Não foram criados usuários, tokens ou chamados para contornar essa limitação.

Os **20 testes unitários das duas funções publicadas passaram no Xano**: cinco de `get_actor_scope` e quinze de `require_ticket_read`. Cobrem leitura técnica global (inclusive chamado de outro técnico e sem associação), associações legadas e múltiplas, regressões de administrador/gestor e bloqueio de funcionário em chamado alheio. Esses testes usam mocks e não substituem os testes autenticados dos endpoints ou de concorrência.

## Validação funcional informada pelo usuário em 20/10/2026

Após configurar a URL do Xano e testar a aplicação, o usuário informou: “realizei os testes tudo funcional”. O relato registra a aprovação funcional do uso testado pelo usuário; não representa execução de testes pelo agente.

Não foram detalhados os cenários, dispositivos, perfis ou requisições utilizados. Portanto, o relato não comprova individualmente testes de concorrência, tentativas de acesso indevido por requisição direta, compatibilidade de consultas sem filtro ou layout móvel. As tarefas que exigem essas verificações permanecem abertas, sem invalidar a aprovação funcional recebida.

## Pendências antes de considerar a mudança concluída

- Executar testes Xano da política de leitura e das interações após disponibilizar os contratos em ambiente autorizado.
- Executar a matriz real de operações existentes (assumir/comentar/PATCH), incluindo concorrência entre autoassociação e conclusão. O endpoint atual verifica `Aberto` antes de criar o vínculo; não foi comprovada atomicidade entre essa leitura e a gravação. A tarefa 1.3 permanece pendente, e não se afirma que esse risco foi resolvido.
- Verificar visualmente a aplicação em desktop e móvel e executar o fluxo com autenticação real, incluindo regressão do funcionário.
- A publicação dos seis contratos e a conferência do export remoto estão realizadas. Não arquivar a mudança enquanto as demais validações estiverem pendentes.
