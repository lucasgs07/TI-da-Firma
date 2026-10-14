# Tasks

## 1. ConfiguraÃ§Ã£o e contrato Xano

- [x] 1.1 Confirmar a URL-base e os caminhos finais de `auth/login` e `auth/me` na especificaÃ§Ã£o da API Xano do ambiente, configurar a URL-base fora dos arquivos versionados e documentar a configuraÃ§Ã£o; verificar inicializaÃ§Ã£o com configuraÃ§Ã£o vÃ¡lida e erro claro quando ausente.
- [x] 1.2 Implementar o acesso aos endpoints de autenticaÃ§Ã£o com tratamento distinto para credenciais rejeitadas e falhas de comunicaÃ§Ã£o; verificar respostas simuladas de sucesso, rejeiÃ§Ã£o e indisponibilidade sem expor senha ou token em logs ou mensagens.

## 2. Login e contexto seguro de usuÃ¡rio

- [x] 2.1 Substituir a pÃ¡gina de exemplo por uma tela de login com e-mail, senha, envio e estados de carregamento/erro; verificar login vÃ¡lido, credenciais invÃ¡lidas e falha de rede.
- [x] 2.2 Ao autenticar, guardar o token e somente os campos seguros retornados do usuÃ¡rio (`id`, `name`, `email`, `perfil_id`, `departamento_id`); verificar que senha e outros dados secretos nÃ£o persistem nem aparecem na interface ou nos logs.

## 3. RestauraÃ§Ã£o e proteÃ§Ã£o da sessÃ£o

- [x] 3.1 Persistir token e perfil seguro entre reinicializaÃ§Ãµes do navegador e validar o token com `auth/me` antes de mostrar conteÃºdo autenticado; verificar restauraÃ§Ã£o vÃ¡lida apÃ³s recarregar e reabrir o navegador.
- [x] 3.2 Proteger a pÃ¡gina inicial autenticada e tratar tokens rejeitados e falhas transitÃ³rias de rede sem revelar conteÃºdo protegido; verificar acesso direto sem sessÃ£o, sessÃ£o expirada e recuperaÃ§Ã£o apÃ³s indisponibilidade.
- [x] 3.3 Disponibilizar o token no cabeÃ§alho exigido pelo Xano para chamadas autenticadas futuras; verificar uma chamada protegida simulada e garantir que o token nÃ£o seja incluÃ­do em URL ou logs.

## 4. Logout e validaÃ§Ã£o integrada

- [x] 4.1 Implementar logout local que remova token, perfil e estado autenticado e redirecione ao login, sem alegar revogaÃ§Ã£o remota; verificar que a sessÃ£o local deixa de acessar pÃ¡ginas protegidas e registrar a validade residual de atÃ© 24 horas na documentaÃ§Ã£o da funcionalidade.
- [x] 4.2 Executar a verificaÃ§Ã£o integrada do app Reflex e percorrer login, restauraÃ§Ã£o, proteÃ§Ã£o, falhas de autenticaÃ§Ã£o e logout; confirmar compilaÃ§Ã£o/inicializaÃ§Ã£o e que nenhuma etapa depende de revogaÃ§Ã£o de token no Xano.
