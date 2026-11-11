# SLA de chamados

## Política

O campo `sla_horas` da prioridade aceita somente `12`, `36`, `50` ou `null`. Os valores aprovados são:

| Prioridade | SLA |
|---|---:|
| Alta | 12 horas |
| Média | 36 horas |
| Baixa | 50 horas |

O prazo conta todas as horas dos dias de segunda a sexta-feira, inclusive à noite. O calendário usa `America/Sao_Paulo` e pausa fins de semana e feriados nacionais definidos em lei federal: 1º de janeiro, 21 de abril, 1º de maio, 7 de setembro, 12 de outubro, 2 de novembro, 15 de novembro, 20 de novembro e 25 de dezembro. Sexta-feira Santa, Carnaval e Corpus Christi não são tratados como feriados nacionais.

Se o chamado for criado ou tiver a prioridade alterada em um dia não útil, a contagem começa às 00:00 do próximo dia útil. Uma alteração de prioridade reinicia a duração integral do SLA usando a nova prioridade. Prioridades com `sla_horas` nulo não geram prazo.

## Contratos Xano

- `GET /prioridade` inclui `sla_horas` na resposta.
- `POST /prioridade` e `PATCH /prioridade/{prioridade_id}` permitem que administradores configurem `sla_horas`; somente `12`, `36`, `50` e `null` são aceitos.
- `POST /chamado` calcula o prazo no backend e retorna `sla_horas`, `sla_inicio_em` e `prazo_sla`.
- `PATCH /chamado/{chamado_id}/prioridade` permite que gestores e administradores alterem a prioridade dentro do escopo de acesso existente. O backend recalcula o prazo e ignora prazos enviados pelo cliente.
- As respostas autenticadas de chamados incluem `sla_inicio_em` e `prazo_sla`; ambos ficam nulos quando não há SLA aplicável ou quando o registro ainda não foi inicializado.

Os registros de prioridade já existentes precisam ser conferidos e configurados antes de o indicador de atraso depender do SLA. Chamados anteriores à ativação também precisam de uma decisão de migração; nenhum backfill de registros será executado implicitamente.
