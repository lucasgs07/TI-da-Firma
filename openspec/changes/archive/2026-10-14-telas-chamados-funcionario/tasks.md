# Tasks

## 1. Contratos Xano e cliente HTTP

- [x] 1.1 Conferir no Xano remoto, sem escrita, se os endpoints exportados de lista, detalhe, abertura, categorias e prioridades estão publicados e exigem autenticação; confirmar que o perfil 4 só consulta chamados próprios e que solicitante/status são definidos no servidor. Verificação: leitura do workspace remoto confirmou os endpoints protegidos por autenticação e as regras de escopo/solicitante/status; nenhuma alteração remota foi executada.
- [x] 1.2 Conferir se `categoria_chamado` contém os pares `1 - Hardware`, `2 - Software`, `3 - Rede`, `4 - Acesso`, `5 - Impressora` e `6 - Outros`. Verificação: o usuário confirmou que esses seis registros já existem; não foram inseridos nem alterados registros remotamente.
- [x] 1.3 Estender o cliente HTTP com consultas autenticadas de chamados, detalhe, abertura, categorias e prioridades, tratando respostas de lista/objeto e falhas sem sucesso implícito. Verificação: os testes HTTP direcionados em `tests/test_xano_client.py` passaram (14 testes), cobrindo métodos, rotas, token, payload e respostas inválidas.

## 2. Área autenticada do funcionário

- [x] 2.1 Implementar a navegação e o estado de consulta dos chamados para `perfil_id` 4, incluindo carregamento, lista vazia, atualização e erro. Verificação: testes do estado cobrem funcionário, lista vazia, falha de serviço e atualização; o escopo dos registros vem do backend.
- [x] 2.2 Implementar o detalhe do chamado próprio e limpar dados anteriores quando a consulta for negada ou falhar. Verificação: testes cobrem detalhe permitido e resposta negada, confirmando que dados anteriores são removidos.
- [x] 2.3 Bloquear as telas exclusivas de funcionário para perfis diferentes de 4 sem afetar a página autenticada genérica existente. Verificação: o perfil 4 é o único que recebe a área do funcionário na página autenticada; chamadas dos eventos de lista e abertura são bloqueadas para outros perfis.
- [x] 2.4 Adicionar testes para estado de carregamento, lista vazia, erro de API, detalhe autorizado/negado e bloqueio por perfil. Verificação: os testes de estado foram executados junto à suíte completa; Reflex compilou sem erros.

## 3. Abertura de chamado e categorias

- [x] 3.1 Implementar o formulário de abertura com título, descrição, categoria e prioridade carregadas pelas APIs autenticadas, submetendo os identificadores retornados pelo Xano. Verificação: o fluxo simulado carrega as seis categorias e prioridades do Xano, seleciona IDs das respostas e envia somente os campos editáveis; solicitante e status são derivados pelo backend.
- [x] 3.2 Tratar validação de campos, opções ausentes, envio bem-sucedido, rejeição e indisponibilidade sem perder os dados digitados nem anunciar sucesso incorretamente. Verificação: testes cobrem lookups indisponíveis, entradas inválidas, criação bem-sucedida, rejeição e falha de rede; o formulário não é limpo no erro e a lista é atualizada após sucesso.

## 4. Validação integrada

- [x] 4.1 Validar o fluxo completo com dados de teste: login de funcionário, leitura apenas dos próprios chamados, abertura com categoria/prioridade válidas e consulta do detalhe; executar também uma tentativa de leitura cruzada com resultado negado. Verificação: teste integrado com transporte Xano simulado passou para abertura/lista/detalhe e negação de outro ID; nenhum registro de produção foi criado.
- [x] 4.2 Verificar a aplicação Reflex e regressões dos fluxos existentes de login, restauração de sessão e logout. Verificação: suíte completa passou (33 testes), login/restauração/logout foram exercitados e `reflex compile` concluiu com sucesso.

## 5. Compatibilidade com as opções do Xano publicado

- [x] 5.1 Remover a exigência de correspondência exata com os seis pares inicialmente informados e aceitar categorias válidas retornadas pelo Xano. Verificação: teste de regressão cobre opções com IDs e quantidade diferentes e confirma que o envio usa o ID retornado pelo lookup.
