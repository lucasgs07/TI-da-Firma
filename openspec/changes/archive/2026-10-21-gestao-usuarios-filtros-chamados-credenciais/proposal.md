# Proposal

## Why

O administrador consegue cadastrar pessoas, mas não possui lista e edição completas de usuários. Os filtros de chamados variam por portal, dificultando localizar solicitações dentro dos escopos autorizados.

## What Changes

- Listar todos os usuários para o administrador, com navegação completa, detalhe e edição de nome, e-mail, perfil, departamento e status Ativo/Inativo.
- Aplicar no backend o status de acesso e as alterações de perfil/departamento, inclusive para sessões já emitidas. Preservar integridade das associações existentes.
- Oferecer prioridade, status e pesquisa por nome do solicitante em todos os portais de chamados, sem ampliar permissões de leitura ou atendimento.
- Preservar o cadastro com senha definida manualmente por administradores e gestores, sem geração automática, padrão fixo ou envio da senha inicial por e-mail.
- Não incluir exclusão de usuários, edição por gestores, novos poderes de atendimento, geração automática de senhas, recuperação/redefinição de senha ou troca obrigatória no primeiro acesso.

## Capabilities

### New Capabilities

- `user-management`: listagem e edição administrativas, preservando o cadastro com senha manual.
- `ticket-search`: filtros combinados e consistentes nos quatro perfis, respeitando os escopos existentes.

### Modified Capabilities

- `user-authentication`: rejeitar contas inativas no login e nas chamadas autenticadas, reavaliando o perfil e departamento atuais.
- `manager-portal`: preservar senha manual e restrições do cadastro gerencial durante a entrega das novas funcionalidades.

## Impact

Reflex: `admin_portal.py`, `admin_state.py`, `office_portal.py`, `office_state.py`, `auth_state.py`, `technician_portal.py`, `TI_da_Firma.py` e `xano_client.py`. Xano: reutilizar `users/directory`, `users/create`, consulta de chamados, autenticação, helpers de autorização; propor detalhe/PATCH administrativos sem duplicar tabelas. Manter fontes em `apis/`, `functions/` e exportações em `database/xano-export/` consistentes.

O inventário principal do OpenSpec contém apenas autenticação, portal gerencial e portal do funcionário. Os contratos administrativos e técnicos estão documentados em mudanças arquivadas; serão preservados, sem editar esses arquivos históricos.

Pendências técnicas específicas: confirmar serialização das edições administrativas e validar concorrência no ambiente Xano antes da publicação. Recuperação de senha foi retirada desta mudança por decisão do usuário; não há dependência de serviço de e-mail nesta entrega. A publicação remota exige `--dry-run`, apresentação do impacto e autorização explícita.
