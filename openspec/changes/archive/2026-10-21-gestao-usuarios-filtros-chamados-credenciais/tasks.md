# Tasks

## 1. Contratos administrativos e status

- [x] 1.1 Ampliar a projeção administrativa de `users/directory` e adicionar GET de usuário por ID, preservando seletores gerenciais; testar paginação global, e-mail somente para admin e negação aos outros perfis, mantendo fontes/exportações equivalentes.
- [x] 1.2 Implementar PATCH administrativo com whitelist, e-mail único, referências existentes, técnico em T.I. e preservação das associações; testar alterações válidas, rejeições sem gravação parcial e impossibilidade de enviar senha ou ID.
- [x] 1.3 Implementar proteção transacional do último admin ativo e verificar mecanismo de concorrência suportado; validar duas inativações/rebaixamentos simultâneos sem perda do último administrador.
- [x] 1.4 Aplicar status Inativo e identidade atual em login, `auth/me` e helpers protegidos; testar conta inativa com senha válida, token anterior à inativação, mudança de perfil/departamento e compatibilidade de status legado vazio.
- [x] 1.5 Documentar contratos, campos seguros e efeitos do status em `docs/portal-admin.md` e documentação de sessão; conferir a documentação contra os testes das tarefas 1.1–1.4.

## 2. Listagem e edição no Reflex

- [x] 2.1 Acrescentar métodos do cliente e estado administrativo para lista paginada, detalhe e edição sem expor dados de outros perfis; testar payloads permitidos, paginação e limpeza no logout/rejeição.
- [x] 2.2 Implementar lista de usuários e formulário de edição com os cinco campos aprovados, preservando cadastro; validar salvar/recarregar, erro de e-mail duplicado, status e bloqueio de envio simultâneo, com testes do estado e compilação Reflex.
- [x] 2.3 Atualizar guia administrativo de uso e conferir que cadastro, lista, detalhe, edição e resultado de falha correspondem aos controles implementados.

## 3. Pesquisa de chamados

- [x] 3.1 Acrescentar os três filtros opcionais ao GET de chamados e aplicá-los por interseção após o escopo; testar IDs inválidos, trim, limite de nome, combinação de filtros e ausência de filtros para os quatro perfis.
- [x] 3.2 Conectar cliente, estados e controles Aplicar/Limpar de admin, gestor, técnico e funcionário, preservando número/título; testar propagação de parâmetros, retorno vazio versus erro e limpeza entre sessões.
- [x] 3.3 Cobrir testes negativos de acesso com nome de solicitante externo e regressão das ações técnicas por associação/status/solução; verificar que filtro nunca altera permissões de escrita.
- [x] 3.4 Documentar filtros, escopos e uso em cada portal; validar exemplos de consulta contra os contratos e compilar os quatro portais.

## 4. Preservação do cadastro com senha manual

- [x] 4.1 Preservar `users/create` e formulários de admin/gestores com senha manual; testar as regras de senha, escopos e ausência de credenciais em respostas, logs e armazenamento persistente, sem geração ou envio automático.
- [x] 4.2 Documentar que o cadastro permanece manual e independente de e-mail e que recuperação de senha está fora do escopo; conferir a documentação contra os contratos e formulários existentes.

## 5. Integração e publicação autorizada

- [x] 5.1 Executar suíte Python e `reflex compile --dry`; registrar resultados e testar os fluxos integrados dos quatro perfis, incluindo paginação, edição durante sessão, filtros, cadastro manual, sem tratar simulação local como validação remota.
- [x] 5.2 Conferir fontes/exportação e produzir `xano workspace push --dry-run` somente dos contratos desta mudança; apresentar saída e impacto, aguardando autorização explícita antes de qualquer gravação remota.
- [x] 5.3 Após autorização, publicar contratos e frontend coordenadamente e verificar exportações, autorização, listagem/edição de usuários e filtros dos quatro perfis; registrar evidências sem senha e manter pendentes os testes não executados.

## Encerramento confirmado pelo responsável

Em 21/10/2026, o usuário confirmou que as tarefas anteriormente pendentes estão concluídas e autorizou marcá-las e arquivar com sincronização das specs. Validações externas são registradas por confirmação do usuário; não foram reexecutadas pelo agente. Evidências locais: 178 testes Python e compilação Reflex bem-sucedidos.
