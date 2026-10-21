# Gestão de usuários e filtros — implementação em andamento

Mudança: `gestao-usuarios-filtros-chamados-credenciais`.

## Implementação local

- Área Usuários com listagem paginada, cadastro manual preservado e edição de nome, e-mail, perfil, departamento e status. Opções vêm dos cadastros existentes; técnico pertence a T.I. Administrador pode não possuir departamento.
- Cliente e estado com whitelist de escrita, checagem da identidade das respostas, rejeição de paginação inconsistente, bloqueio de envios simultâneos e limpeza de dados no logout.
- Contratos GET/PATCH administrativos de usuário e projeção de e-mail exclusiva do admin no diretório; seletores gerenciais preservados.
- Login e contexto do ator com verificação de Inativo; rotas operacionais auxiliares selecionadas passam pelo helper de contexto. A rejeição de conta inativa usa 401 para limpar sessão também no transporte operacional. Os endpoints legados de recuperação estão fora deste escopo e não foram alterados.
- Filtros de prioridade, status e nome do solicitante nos quatro portais. Aplicar consulta o backend; Limpar remove os filtros e recarrega. Número/título refinam os resultados autorizados. As opções usam IDs existentes; o cliente detecta respostas que ignoram filtros. O funcionário possui guarda adicional contra registros de outro solicitante.
- Recuperação de senha, geração automática e envio de credenciais por e-mail foram retirados do escopo por decisão do usuário.

## Evidências locais em 21/10/2026

- `python -m pytest tests -q -p no:cacheprovider`: 178 testes passaram, incluindo os novos testes de gestão e filtros.
- `reflex compile --dry`: compilação concluída.
- `openspec validate gestao-usuarios-filtros-chamados-credenciais --strict`: válido.
- `git diff --check` nos arquivos de implementação/documentação: sem erros.
- Conferidos 23 pares fonte/exportação locais. Nenhuma tabela, registro ou variável foi selecionada.
- Os testes Python usam transporte/estado simulados; não executam XanoScript nem comprovam autorização, persistência ou concorrência remotas. Não houve inspeção visual no navegador nesta etapa.

## Simulação de publicação

`xano workspace push --dry-run` com seleção explícita de 23 arquivos retornou:

```text
Matched: 23 of 204 files
Functions            ~1 updated
API Endpoints        +2 created  ~20 updated
UPDATE function helpdesk/access/get_actor_context
CREATE query users/{user_id} GET
CREATE query users/{user_id} PATCH
```

As outras atualizações abrangem login, diretório, GET de chamados e a verificação central do ator em consultas auxiliares/rotas operacionais que ainda não usavam helpers. O detalhamento completo está na saída do CLI desta sessão. Não foram usadas opções de exclusão, sincronização destrutiva, registros, variáveis de ambiente ou sobrescrita forçada. A simulação não publicou contratos.

## Pendências de conclusão

O PATCH prepara `db.transaction` e bloqueio do registro existente do perfil administrativo para serializar edições. A sintaxe/opção `lock` no runtime alvo, a rejeição de campos extras e duas edições concorrentes ainda precisam ser validadas no Xano. O preview do CLI não substitui esses testes. Não considerar a proteção do último admin validada apenas pelos testes Python.

A consulta de branches retornou somente `v1`, com `live: true`. Nenhuma branch ou workspace isolado foi criado. Não executar testes destrutivos contra usuários reais; qualquer teste com mutação exige ambiente/dados de teste autorizados.

Continuam pendentes os testes autenticados de leitura/edição/filtros, status de conta, preservação das associações e concorrência. A publicação autorizada e a conferência remota foram realizadas conforme o registro abaixo. As tarefas que incluem verificações ainda não executadas permanecem abertas; a mudança não foi arquivada.

## Publicação autorizada — 21/10/2026

Após autorização explícita do usuário, os 23 contratos foram publicados na branch `v1` do workspace 147362: `Pushed 23 documents ... in 4.0s`. O CLI não interativo exigiu `--force` para substituir sua confirmação de terminal; não foram usadas exclusões, importação de registros/variáveis ou desativação da transação.

O CLI retornou alertas de referências não resolvidas. Duas exportações remotas posteriores, sem registros ou variáveis, confirmaram os 23 contratos sem placeholders, as tabelas e funções referenciadas existentes e a preservação de `db.transaction`/`lock = true` no PATCH. Fontes e pares em `database/xano-export` foram alinhados ao export remoto, normalizando apenas espaços finais.

A verificação sem autenticação detectou que os IDs opcionais de filtro precisavam de tipo nullable: sem isso, ausência virava zero e causava erro 400 antes da autenticação. Após nova simulação restrita (`~1 updated`), a correção de `chamado GET` foi publicada dentro do escopo autorizado e conferida no export final. Sem filtros, com solicitante ou com IDs válidos, a consulta sem credenciais retorna 401; prioridade zero retorna 400. `auth/me`, `users/directory` e `users/1` sem credenciais retornaram 401.

Depois da publicação: 178 testes Python passaram, Reflex compilou e `git diff --check` não apontou erros. A publicação e a conferência remota descritas acima estão realizadas; continuam pendentes os testes autenticados dos quatro perfis, persistência/negações do PATCH, bloqueio real de conta Inativa, concorrência do último administrador e inspeção visual. A tarefa 5.3 permanece aberta porque inclui essas verificações, não apenas importar contratos. Nenhuma conta foi criada, editada ou inativada para testes nesta etapa.

## Arquivos afetados

- Reflex: `TI_da_Firma/TI_da_Firma.py`, `admin_portal.py`, `admin_state.py`, `auth_state.py`, `office_portal.py`, `office_state.py`, `technician_portal.py`, `xano_client.py` e novo `ticket_filters.py`.
- Testes: novos `tests/test_user_management.py` e `tests/test_ticket_filters.py`.
- Backend: 22 contratos de API em `apis/` e o helper de contexto em `functions/`, com seus pares em `database/xano-export/`.
- Documentação: este registro, guias administrativo/técnico/gerencial/de sessão e checklist da mudança OpenSpec.
