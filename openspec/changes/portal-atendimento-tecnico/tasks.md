# Tasks

## 1. Contratos e autorização no Xano

- [ ] 1.1 Alinhar `get_actor_scope`, `require_ticket_read` e GET de lista/detalhe de chamados à leitura global do perfil 3; atualizar os testes Xano para chamados de outros técnicos e finalizados e executar regressões de funcionário/gestor/admin, comprovando que a escrita continua restrita.
- [ ] 1.2 Ajustar leitura de interações e GET individual para a mesma autorização, adicionar filtro opcional `chamado_id` no GET de lista e nome público do autor; validar testes de filtro, ordenação, ausência de dados privados e compatibilidade sem filtro.
- [ ] 1.3 Verificar os endpoints existentes de assumir, comentar e PATCH contra a especificação, corrigindo apenas lacunas: testar identidade adulterada, associação múltipla/idempotente, legado, concorrência com conclusão, técnico não associado, solução obrigatória, status ausente e bloqueio operacional após conclusão.
- [x] 1.4 Manter `apis/`, `functions/` e `database/xano-export/` coerentes e documentar contratos e matriz de permissões desta entrega; verificar diff sem alterações de esquema ou credenciais.

## 2. Integração HTTP e estado da aplicação

- [x] 2.1 Após o grupo 1, estender `xano_client.py` para histórico filtrado, autoassociação, comentário e atualização de status/solução, sem aceitar identidade do ator; verificar métodos, caminhos, payloads e erros com testes HTTP simulados em `tests/`.
- [x] 2.2 Criar o fluxo de estado técnico integrado à validação de sessão, preservando verificações exclusivas do funcionário; testar perfil 3, acesso indevido, restauração, logout, expiração e limpeza ao trocar chamado.
- [x] 2.3 Implementar eventos de atendimento com bloqueio de envios simultâneos, mensagens de erro, preservação de texto e recarga dos dados após sucesso; testar API rejeitada, falha de rede e ausência de confirmação falsa.
- [x] 2.4 Documentar o fluxo de sessão e as novas ações técnicas junto da documentação pertinente; conferir exemplos contra os contratos e executar os testes existentes de cliente e portal do funcionário.

## 3. Interface do técnico

- [x] 3.1 Após o grupo 2, apresentar a lista global ao técnico após login, com número/título, status, solicitante, categoria, prioridade e técnicos; validar renderização, abertura de detalhes e estados vazio/carregando/erro.
- [x] 3.2 Implementar detalhe com contexto do solicitante, descrição, técnicos, solução e histórico cronológico com autor/data, inspirado na organização funcional do GLPI; validar chamado alheio/finalizado, histórico vazio e erro independente do histórico.
- [x] 3.3 Conectar autoassociação, comentário, status e solução aos eventos autorizados, distinguindo consulta de edição e usando `Em atendimento` para iniciar; verificar cenários de associação existente, chamado não aberto, técnico não associado e finalização sem solução.
- [ ] 3.4 Compilar conforme `reflex-process-management` e realizar verificação visual em largura desktop e móvel, incluindo regressão da área do funcionário; registrar resultados e corrigir erros de compilação ou disposição que impeçam as ações.

## 4. Integração com ambiente autorizado

- [x] 4.1 Comparar os contratos locais com o ambiente Xano disponível sem gravar remotamente; entregar registro das diferenças e simulação das mudanças. Se usar `xano workspace push`, executar primeiro `--dry-run` e apresentar sua saída, aguardando autorização explícita antes da publicação.
- [ ] 4.2 Somente após autorização, aplicar as mudanças remotas e conferir exportação/contratos; validar leitura global do técnico, restrições dos demais perfis e rejeição de escrita não autorizada por requisição direta.
- [ ] 4.3 Executar o fluxo integrado login técnico → consulta global → detalhe/solicitante → autoassociação em aberto → comentário → em atendimento → conclusão com solução; conferir persistência após recarga, regressão do funcionário e registrar testes realizados e limitações, sem marcar integração remota concluída quando não executada.

## Registro de execução

Ver `docs/portal-tecnico.md` para resultados e a simulação remota. As tarefas 1.1 e 1.2 têm os contratos publicados; os 20 testes dos helpers passaram no Xano, mas faltam verificações específicas dos endpoints. A tarefa 1.3 depende também da verificação de concorrência. A compilação de 3.4 passou, mas o agente não realizou QA visual. A publicação autorizada dos seis contratos e a conferência da exportação remota foram realizadas. Os 68 testes Python passaram; o fluxo integrado automatizado usou HTTP simulado.

### Validação do usuário — 20/10/2026

O usuário informou que realizou os testes e encontrou tudo funcional, autorizando o registro dessa validação. A aprovação funcional está registrada também em `docs/portal-tecnico.md`, com atribuição ao usuário.

O relato não detalha cenários ou dispositivos. Por isso, não foram marcadas como concluídas tarefas que também exigem concorrência, matriz de autorização por requisição direta, compatibilidade sem filtro, regressão de outros perfis e verificação móvel. As tarefas 1.1, 1.2, 1.3, 3.4, 4.2 e 4.3 continuam parcialmente verificadas. A mudança permanece ativa, sem arquivamento, até concluir essas verificações conforme as regras do projeto.
