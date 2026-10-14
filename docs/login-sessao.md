# Login e sessão no Reflex

## Configuração

Configure `XANO_API_BASE_URL` no arquivo `.env` da raiz do projeto. O cliente Xano carrega esse arquivo automaticamente ao iniciar; `.env` é ignorado pelo Git. Use `.env.example` como modelo e mantenha a URL real apenas no arquivo local.

```powershell
uv run reflex run --env prod --single-port
```

Uma variável `XANO_API_BASE_URL` já definida no ambiente do processo tem precedência sobre o valor do arquivo `.env`. Sem uma URL configurada, o login mostra um erro de configuração.

## Comportamento

- `/login` autentica via `auth/login`; `/` é protegida e valida o token com `auth/me`.
- Após o login, funcionários (`perfil_id` 4) seguem para `/chamados/novo`; os demais perfis seguem para `/`.
- O token e o perfil seguro (`id`, `name`, `email`, `perfil_id`, `departamento_id`) ficam no `LocalStorage` e sobrevivem ao fechar o navegador.
- Token rejeitado limpa a sessão e leva ao login; falha de rede mostra erro com "Tentar novamente".
- Chamadas futuras ao Xano usam `AuthState.get_auth_headers()` (`Authorization: Bearer <token>`).

## Logout e validade residual

O logout é **local**: remove token, perfil e estado do navegador. O Xano não revoga tokens, então um token copiado antes do logout continua válido até expirar (**até 24 horas**).

## Risco conhecido

O `LocalStorage` é acessível por scripts da página (risco de XSS). Evite incluir scripts de terceiros no app.
