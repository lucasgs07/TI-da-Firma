# Preparação do commit

Mensagem sugerida: feat: adiciona gestão de usuários e filtros de chamados com visual Nexo

Escopo: frontend Reflex, componentes visuais Nexo, listagem/edição administrativa, filtros dos quatro perfis, contratos Xano publicados, exportações correspondentes, testes e documentação.

Verificações locais mais recentes: 178 testes passaram; reflex compile --dry concluído.
Encerramento: o usuário confirmou a conclusão das tarefas anteriormente pendentes. OpenSpec: 17/17, com registro da origem dessa confirmação. Validações externas não foram reexecutadas pelo agente.

Não incluir: .env, .xano, logs, caches, ferramentas/skills de agentes nem movimentações antigas de outras mudanças.
Nenhum commit ou push Git executado.
Mudança arquivada em 21/10/2026, com quatro specs sincronizadas e validadas.

## Arquivos selecionados

- TI_da_Firma/TI_da_Firma.py
- TI_da_Firma/admin_portal.py
- TI_da_Firma/admin_state.py
- TI_da_Firma/auth_state.py
- TI_da_Firma/design.py
- TI_da_Firma/office_portal.py
- TI_da_Firma/office_state.py
- TI_da_Firma/shell.py
- TI_da_Firma/technician_portal.py
- TI_da_Firma/ticket_filters.py
- TI_da_Firma/xano_client.py
- apis/authentication/4091243_auth_login_POST.xs
- apis/authentication/4091252_perfil_perfil_id_GET.xs
- apis/authentication/4091253_perfil_GET.xs
- apis/authentication/4091258_departamento_departamento_id_GET.xs
- apis/authentication/4091259_departamento_GET.xs
- apis/authentication/4091265_prioridade_prioridade_id_GET.xs
- apis/authentication/4091266_prioridade_GET.xs
- apis/authentication/4091274_tipo_ativo_tipo_ativo_id_GET.xs
- apis/authentication/4091275_tipo_ativo_GET.xs
- apis/authentication/4091287_status_ativo_status_ativo_id_GET.xs
- apis/authentication/4091288_status_ativo_GET.xs
- apis/authentication/4091305_status_chamado_status_chamado_id_GET.xs
- apis/authentication/4091306_status_chamado_GET.xs
- apis/authentication/4091310_categoria_chamado_categoria_chamado_id_GET.xs
- apis/authentication/4091311_categoria_chamado_GET.xs
- apis/authentication/4091329_chamado_GET.xs
- apis/authentication/4091346_interacao_chamado_interacao_chamado_id_DELETE.xs
- apis/authentication/4091350_interacao_chamado_interacao_chamado_id_PATCH.xs
- apis/authentication/4092063_users_directory_GET.xs
- apis/authentication/users_user_id_GET.xs
- apis/authentication/users_user_id_PATCH.xs
- apis/event_logs/4091246_logs_user_my_events_GET.xs
- assets/nexo.css
- database/xano-export/api/authentication/auth/login_POST.xs
- database/xano-export/api/authentication/categoria_chamado/categoria_chamado_id_GET.xs
- database/xano-export/api/authentication/categoria_chamado_GET.xs
- database/xano-export/api/authentication/chamado_GET.xs
- database/xano-export/api/authentication/departamento/departamento_id_GET.xs
- database/xano-export/api/authentication/departamento_GET.xs
- database/xano-export/api/authentication/interacao_chamado/interacao_chamado_id_DELETE.xs
- database/xano-export/api/authentication/interacao_chamado/interacao_chamado_id_PATCH.xs
- database/xano-export/api/authentication/perfil/perfil_id_GET.xs
- database/xano-export/api/authentication/perfil_GET.xs
- database/xano-export/api/authentication/prioridade/prioridade_id_GET.xs
- database/xano-export/api/authentication/prioridade_GET.xs
- database/xano-export/api/authentication/status_ativo/status_ativo_id_GET.xs
- database/xano-export/api/authentication/status_ativo_GET.xs
- database/xano-export/api/authentication/status_chamado/status_chamado_id_GET.xs
- database/xano-export/api/authentication/status_chamado_GET.xs
- database/xano-export/api/authentication/tipo_ativo/tipo_ativo_id_GET.xs
- database/xano-export/api/authentication/tipo_ativo_GET.xs
- database/xano-export/api/authentication/users/directory_GET.xs
- database/xano-export/api/authentication/users/user_id_GET.xs
- database/xano-export/api/authentication/users/user_id_PATCH.xs
- database/xano-export/api/event_logs/logs/user/my_events_GET.xs
- database/xano-export/function/helpdesk/access/get_actor_context.xs
- docs/figma/04-funcionario-detalhe.md
- docs/figma/06-tecnico-atendimento.md
- docs/figma/11-administrador-cadastro.md
- docs/figma/15-mobile-abrir-chamado.md
- docs/figma/16-estados-interface.md
- docs/gestao-usuarios-implementacao.md
- docs/login-sessao.md
- docs/nexo-figma.md
- docs/portal-admin.md
- docs/portal-gerencial.md
- docs/portal-tecnico.md
- functions/helpdesk/access/351524_get_actor_context.xs
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/.openspec.yaml
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/design.md
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/proposal.md
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/specs/manager-portal/spec.md
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/specs/ticket-search/spec.md
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/specs/user-authentication/spec.md
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/specs/user-management/spec.md
- openspec/changes/archive/2026-10-21-gestao-usuarios-filtros-chamados-credenciais/tasks.md
- rxconfig.py
- tests/test_ticket_filters.py
- tests/test_user_management.py

- openspec/specs/manager-portal/spec.md
- openspec/specs/ticket-search/spec.md
- openspec/specs/user-authentication/spec.md
- openspec/specs/user-management/spec.md
