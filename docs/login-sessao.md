# Login e sessão no Reflex

## Configuração

Defina a URL base do grupo de API Authentication do Xano (veja `.env.example`):

```powershell
$env:XANO_API_BASE_URL="https://<instancia>.xano.io/api:YVgiBQ2M"
.\.venv\Scripts\reflex.exe run
```

Sem a variável, o login mostra um erro de configuração.

## Comportamento

- `/login` autentica via `auth/login`; `/` é protegida e valida o token com `auth/me`.
- O token e o perfil seguro (`id`, `name`, `email`, `perfil_id`, `departamento_id`) ficam no `LocalStorage` e sobrevivem ao fechar o navegador.
- Token rejeitado limpa a sessão e leva ao login; falha de rede mostra erro com "Tentar novamente".
- Chamadas futuras ao Xano usam `AuthState.get_auth_headers()` (`Authorization: Bearer <token>`).

## Logout e validade residual

Gestores também recebem o [portal gerencial](portal-gerencial.md), conforme seu departamento. Funcionários recebem Minhas tarefas para consultar e concluir tarefas próprias com solução obrigatória, sem autorização para resolver chamados. Os estados dessas áreas são limpos na restauração da sessão e no logout.

O perfil Técnico (3) recebe a área de atendimento após a validação da sessão. Consulte [Portal de atendimento técnico](portal-tecnico.md) para contratos e permissões. Os dados e rascunhos técnicos são limpos no logout e na restauração da sessão; o perfil persistido no navegador é substituído pelo perfil retornado por `auth/me`.

O logout é **local**: remove token, perfil e estado do navegador. O Xano não revoga tokens, então um token copiado antes do logout continua válido até expirar (**até 24 horas**).

## Risco conhecido

O `LocalStorage` é acessível por scripts da página (risco de XSS). Evite incluir scripts de terceiros no app.
