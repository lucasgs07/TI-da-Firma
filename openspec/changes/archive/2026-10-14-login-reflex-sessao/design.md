# Design

## Contexto

Ver [proposal.md](./proposal.md) para a motivação. O projeto contém um app Reflex inicial em `TI_da_Firma/TI_da_Firma.py`, com versão `0.10.0` fixada em `requirements.txt`. O endpoint Xano `auth/login` recebe e-mail e senha e retorna `authToken` e o objeto seguro `user` (`id`, `name`, `email`, `perfil_id`, `departamento_id`). O endpoint autenticado `auth/me` retorna o perfil seguro e permite validar/restaurar uma sessão. O token é emitido com expiração de 24 horas. Não foi encontrado endpoint de logout nem mecanismo de revogação no projeto.

## Objetivos / Não objetivos

**Objetivos:**

- Integrar o primeiro fluxo de autenticação do app Reflex aos endpoints existentes, sem duplicar autenticação no frontend.
- Restaurar e validar a sessão persistida e disponibilizar o perfil mínimo necessário às próximas telas.
- Garantir que páginas e chamadas autenticadas dependam de uma sessão validada.
- Tornar explícita a semântica de logout local e a validade residual do token.

**Não objetivos:**

- Revogar tokens no backend, criar blacklist ou modificar os endpoints protegidos para impor revogação.
- Implementar cadastro, recuperação de senha, renovação de token ou controle de permissões no frontend.
- Criar funcionalidades de negócio ou telas específicas para cada perfil nesta mudança.

## Decisões

1. **Manter Xano como autoridade de autenticação e perfil.** O frontend usa `auth/login` e `auth/me` existentes. Isso evita duplicar regras de senha/perfil e mantém a autorização de dados e operações no backend. Uma autenticação local ou baseada somente no perfil persistido foi descartada por não validar a sessão nem aplicar as políticas Xano.

2. **Persistir token e perfil seguro no armazenamento do navegador com persistência entre reinicializações.** O token é necessário às chamadas seguintes e o requisito pede manter a sessão. O perfil persistido é apenas contexto de interface; deve ser revalidado por `auth/me` e não pode autorizar operações sozinho. Armazenamento apenas em memória ou sessão foi descartado porque encerraria a sessão ao fechar o navegador. A implementação deve usar o recurso de client storage compatível com Reflex `0.10.0` e evitar registrar valores secretos.

3. **Validar o token com `auth/me` antes de apresentar páginas autenticadas.** O token pode expirar mesmo estando salvo. Uma resposta de autenticação inválida encerra a sessão local e leva ao login; falhas de rede não devem ser tratadas silenciosamente como login bem-sucedido nem como prova de que o usuário foi desautenticado. A aplicação deve apresentar erro recuperável e impedir exibir conteúdo protegido enquanto a validação estiver pendente.

4. **Implementar logout somente no cliente nesta mudança.** A pesquisa dos arquivos locais não encontrou endpoint de logout; a autenticação Xano existente emite tokens com validade de 24 horas. Logout apaga o token e o perfil do armazenamento/contexto do navegador, mas não invalida tokens copiados. Revogação remota foi excluída do escopo para evitar introduzir armazenamento e verificações em todos os endpoints protegidos sem projeto aprovado.

5. **Manter configuração de integração fora do código versionado.** A URL-base do grupo de APIs Xano deve vir da configuração de ambiente da aplicação; credenciais e tokens não devem ser embutidos em código ou configuração versionada. O valor e o caminho final de deploy serão fornecidos/verificados no ambiente, não presumidos nesta especificação.

## Riscos / Trade-offs

- **Token persistido no navegador pode ser exposto por XSS ou acesso ao perfil local do navegador** → guardar somente o token necessário e o perfil seguro mínimo; não armazenar a senha; não registrar o token; validar entradas e evitar renderização de conteúdo não confiável. O armazenamento persistente atende ao requisito, mas não oferece proteção equivalente a um cookie HttpOnly.
- **Token permanece utilizável após logout local** → comunicar que a sessão do servidor pode durar até 24 horas; limitar o logout a remover dados locais; considerar mecanismo de revogação/expiração menor como uma mudança futura se o risco não for aceitável.
- **Indisponibilidade de rede durante a restauração da sessão** → não apresentar conteúdo protegido antes da validação nem apagar a sessão como se a API tivesse rejeitado o token; oferecer erro recuperável e nova tentativa.
- **URL ou formato final da API pode variar por ambiente/grupo** → confirmar a especificação e a URL-base Xano no ambiente antes de configurar chamadas; não versionar segredos ou tokens.

## Plano de migração

Não há migração de banco ou de token. Configurar a URL-base do Xano no ambiente antes de disponibilizar o app; usuários sem sessão local deverão entrar normalmente. Rollback consiste em reverter a aplicação frontend. Tokens emitidos continuam sujeitos à expiração original de até 24 horas, inclusive depois de logout local ou rollback.

## Questões em aberto

Nenhuma questão bloqueante. O valor da URL-base do Xano e as URLs públicas por ambiente são dados operacionais a configurar durante a implantação, sem alterar o comportamento especificado.
