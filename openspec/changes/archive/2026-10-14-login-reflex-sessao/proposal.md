# Proposta

## Por que

O frontend Reflex ainda apresenta a página inicial de exemplo e não oferece uma forma de autenticar usuários nem manter o contexto de perfil necessário para as futuras telas. O MVP precisa de um fluxo inicial de login integrado à autenticação já existente no Xano, com persistência de sessão no navegador e uma forma clara de sair.

## O que muda

- Substitui a página inicial de exemplo por um fluxo inicial de login em Reflex.
- Autentica com as credenciais do usuário no endpoint existente do Xano e mantém o token de autenticação e os dados seguros do perfil para uso nas telas e chamadas de API.
- Mantém a sessão entre reinicializações do navegador até o token expirar ou o usuário sair.
- Restringe as páginas autenticadas a usuários com sessão válida e encaminha sessões ausentes ou expiradas ao login.
- Disponibiliza logout que remove do navegador o token e o perfil armazenados.
- Documenta que o logout local não revoga o token no Xano; o token poderá continuar válido até o fim de sua expiração atual, de 24 horas.

## Capacidades

### Novas capacidades

- `user-authentication`: autenticação inicial no frontend, persistência de sessão e contexto seguro de perfil, proteção de páginas e logout local.

### Capacidades modificadas

- Nenhuma capacidade existente foi identificada no inventário de especificações do projeto.

## Impacto

- Frontend Reflex em `TI_da_Firma/TI_da_Firma.py` e configuração existente em `rxconfig.py`.
- Endpoint Xano existente `auth/login`, que retorna `authToken` e uma projeção segura do usuário com `perfil_id` e `departamento_id`.
- Endpoint autenticado existente `auth/me`, que retorna o perfil seguro para validar/restaurar o contexto da sessão.
- Chamadas futuras às APIs Xano autenticadas precisarão enviar o token no cabeçalho de autorização.
- O pacote Reflex está fixado em `requirements.txt` como versão `0.10.0`; a implementação deve usar os recursos compatíveis com essa versão.
- O backend não terá revogação de token nesta mudança. Logout apenas remove os dados locais e não invalida cópias do token já emitido.
