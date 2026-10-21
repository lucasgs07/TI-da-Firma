# Revisão de aderência ao Figma — 21/10/2026

## Resultado e limites

As telas ainda não podem ser consideradas integralmente compatíveis com o Figma. Esta revisão compara o código atual com os cinco contextos exportados em `docs/figma/`, as decisões em `docs/nexo-figma.md` e as imagens fornecidas na conversa. Não é uma aprovação visual.

O conector Figma retornou limite de consultas do plano Starter ao consultar a página `0:1` do arquivo `iogesOf6wVBdGExEIWrx2j`. O inventário de automação retornou `apps: []` e `browsers: []`. Portanto, não foi possível conferir os frames atuais nem navegar pelas telas autenticadas. Nenhum teste funcional ou compilação foi executado nesta revisão; nenhum componente ou endpoint foi alterado.

## Divergências confirmadas

| Prioridade | Tela / componente | Referência e diferença no código |
| --- | --- | --- |
| Alta | Funcionário: detalhe do chamado | Frame `3:192`: relato e resumo em duas colunas, com status em badge. `TI_da_Firma/TI_da_Firma.py`, `_ticket_detail`, mantém um único card em coluna e status em texto. Falta a composição do resumo lateral. |
| Alta | Técnico: atendimento | Frame `3:347`: histórico/comentário à esquerda (744 px) e atendimento à direita (360 px). `technician_portal.py`, `_detail`, coloca `_context()` à esquerda e descrição/histórico à direita, com proporção 1:2. A referência também apresenta ação de resolver separada; a interface atual oferece salvar atendimento e seleção de status. Uma futura adaptação deve preservar as regras existentes. |
| Alta | Administrador: cadastrar usuário | Frame `5:343`: título “Uma nova pessoa na firma.”, campos rotulados, perfil/departamento lado a lado, senha ao final e card “Cada pessoa, sua área.”. `admin_portal.py`, `user_form` e ramo `create` de `users`, apresentam formulário simples em coluna, senha antes de perfil/departamento e sem card lateral. |
| Alta | Funcionário: abrir chamado no celular | Frame `6:169`: formulário direto sobre o fundo e botões em coluna com largura total. `_ticket_form` mantém os dois painéis; `assets/nexo.css` apenas reduz a grade para uma coluna e o padding do card. O painel de dicas continua presente e as ações não recebem largura total. Inputs e textarea já têm alturas globais de 48 e 112 px; a altura dos selects precisa ser conferida. |
| Média | Estados de interface | Frame `6:196`: carregamento com três skeletons de 16 px, validação abaixo do campo, erro com nova tentativa e sucesso com retorno à lista. As telas usam predominantemente spinner/callout e validação nativa; falta a composição completa desses estados. A recuperação de sessão já tem nova tentativa, mas isso não cobre os demais estados. |
| Média | Espaçamento compartilhado | Ainda existem `gap="3"`, `gap="4"` e `gap="5"` em títulos, paginação, ações de formulários e atendimento. Diferentemente de `spacing`, `gap` é estilo CSS e precisa de valor válido com unidade para distâncias não nulas. Esses pontos repetem o padrão dos elementos que apareceram colados nas imagens. Conferir a saída gerada e padronizar com os tokens da referência. |

## Cobertura das telas existentes

| Área | Telas examinadas no código | Situação |
| --- | --- | --- |
| Compartilhada | Navegação desktop/mobile, cabeçalho, títulos, tabelas, badges | Cores, fonte Inter, sidebar de 232 px e barra de 72 px correspondem aos tokens documentados. Há gaps pendentes; renderização e responsividade não validadas. |
| Autenticação | Login e espera/erro de sessão | Estrutura e estilos examinados; sem contexto local completo de frame para certificar fidelidade. |
| Funcionário | Lista, abertura e detalhe de chamado | Lista usa filtros e tabela/cartões compartilhados. Detalhe e abertura mobile têm divergências confirmadas acima. |
| Técnico | Lista e atendimento | Lista usa componentes compartilhados. Atendimento tem colunas invertidas e composição diferente. |
| Funcionário/técnico | Lista e detalhe de tarefas | Estrutura examinada; sem contexto local completo de frame para certificar fidelidade. Lista usa tabela, detalhe usa duas colunas. |
| Gestor | Chamados, abertura, detalhe, cadastro de usuário e criação de tarefa | Estrutura examinada; abertura, cadastro e detalhe ainda usam composições simplificadas. Sem frame local completo específico do gestor para afirmar divergência visual exata. Ações de próximos passos e responsáveis têm gaps sem unidade. |
| Administrador | Dashboard, chamados, tarefas, detalhes, diretório, cadastro, edição e logs | Cadastro diverge do frame exportado. Diretório/edição usam a adaptação documentada por imagens. Demais telas carecem de frame completo e validação renderizada; tarefas e detalhes usam cards/coluna simples. |
| Ajustes desta conversa | Acesso rápido e filtro/exportação de logs | Código já contém as medidas e cores solicitadas nas últimas imagens; ainda sem confirmação no navegador. Estas escolhas posteriores do usuário prevalecem sobre referências anteriores. |

## Diferenças intencionais já documentadas

Não tratar como defeito visual a ausência de dados que o contrato público não fornece: datas/departamento no detalhe do funcionário, data de atualização em sua lista e nome da prioridade de tarefas. Preservar indicação UTC do histórico, escopos por perfil, filtro de solicitante aprovado e dados reais da API. Não preencher lacunas com dados demonstrativos do Figma.

## Ordem sugerida para correção e validação

1. Corrigir espaçamentos compartilhados, conferindo os valores de cada referência.
2. Adaptar detalhe do funcionário, atendimento técnico e cadastro administrativo.
3. Ajustar abertura mobile e padronizar estados de interface.
4. Comparar telas renderizadas nas mesmas dimensões dos frames, incluindo desktop e celular, com sessões dos quatro perfis; conferir também tabelas largas, textos longos e estados vazio/erro/carregamento.
5. Completar os contextos dos demais frames quando o acesso ao Figma estiver disponível. Somente então aprovar aderência visual de todas as telas.

## Continuação da comparação — referências locais e frontend gerado

O acesso foi tentado novamente: o Figma continua retornando limite do plano Starter e o inventário continua sem aplicativos ou navegadores. A comparação abaixo aprofunda as referências já disponíveis; não representa novas capturas do Figma nem validação de pixels no navegador.

### Novos detalhes encontrados

| Item | Referência | Código atual e impacto |
| --- | --- | --- |
| Cadastro: identificação dos campos | `11-administrador-cadastro.md`, nós `5:377` e `5:381`: rótulos persistentes “Nome *” e “E-mail *” | `admin_portal.py`, `user_form`: nome, e-mail e senha têm placeholder e aria-label, mas não rótulo visível separado. Ao preencher, a identificação visual desaparece. |
| Cadastro: instrução de senha | Mesmo frame, nó `5:399`: “Pelo menos 8 caracteres, uma letra e um número.” | O formulário administrativo não mostra essa instrução. O formulário gerencial já tem texto equivalente. Trata-se de comunicação na interface; esta revisão não altera a validação. |
| Detalhe do funcionário: hierarquia | `04-funcionario-detalhe.md`, nós `3:216`, `3:217`, `3:222` e `3:224`: título de 28 px, caminho com número do chamado e subtítulos de 18 px | `_ticket_detail`: título dentro do card com tamanho de tema, sem caminho com ID e sem as mesmas seções. A composição difere mesmo desconsiderando as informações indisponíveis na API. |
| Detalhe do funcionário: retorno | Mesmo frame, nó `3:237`: botão secundário no resumo lateral, largura de 312 px no desktop | O retorno está acima do conteúdo, usa `variant="soft"` e largura automática. |
| Detalhe do funcionário: orientação | Mesmo frame, nó `3:226`: faixa verde suave sobre o atendimento | A faixa não existe no detalhe atual. Ao adaptar, seu texto deve depender do status real; não afirmar atendimento em andamento para qualquer chamado. |
| Atendimento: altura da solução | `06-tecnico-atendimento.md`, nó `3:397`: textarea de 112 px | `_context` define `min_height="8rem"`, em vez de 112 px. É uma divergência de medida declarada; a altura efetiva depende da fonte raiz e precisa de inspeção renderizada. |
| Mobile: largura útil | `15-mobile-abrir-chamado.md`: viewport de 390 px com margens de 20 px e campos de 350 px | O shell respeita as margens de 20 px, mas o formulário ainda recebe borda e padding interno de 20 px do painel. A largura disponível aos campos fica menor que os 350 px da referência. |
| Mobile: conteúdo do formulário | Mesmo frame: título e instrução seguidos diretamente dos campos | O formulário atual ainda mostra o subtítulo interno “Sobre o que você precisa?” e o painel de dicas depois dos campos, ausentes no frame mobile. |
| Barra superior: perfil | Frames desktop exportados, por exemplo `04-funcionario-detalhe.md`, nó `3:212`: perfil em 14 px, peso médio | `shell.py` não define essas propriedades no texto do perfil; ele herda os 12 px da barra e não recebe peso médio. |
| Estado vazio | `16-estados-interface.md`, nó `6:203`: ação de 220 × 44 px e espaços de 20 px | O estado vazio inicial do funcionário tem a ação correta em termos de finalidade, mas sem largura de 220 px; `ui.empty` usa `spacing="4"`. As medidas ainda não reproduzem o frame. |
| Estado de sucesso | Mesmo frame: card “Chamado criado!” com ação “Ver meus chamados” | `AuthState.abrir_chamado` já retorna à lista após o sucesso, e `_employee_portal` mostra um callout. A diferença é a apresentação e a ação explícita, não a ausência de retorno à lista. |

### Confirmação dos gaps sem unidade

A inspeção por AST encontrou **14 ocorrências** de `gap` com string numérica sem unidade nos arquivos Python atuais: seis em `admin_portal.py`, uma em `design.py`, duas em `office_portal.py`, quatro em `technician_portal.py` e uma em `TI_da_Firma.py`.

Nos artefatos já existentes em `.web/app/routes/_index.jsx` e `.web/app/routes/[tarefas]._index.jsx`, o título compartilhado aparece com `css:({ ["gap"] : "4" ... })`. Isso confirma que esse valor é emitido como CSS, em vez de usar a escala de espaçamento do componente. Esses artefatos são de compilação anterior; não foi executada nova compilação nesta revisão.

Não confundir com `spacing="4"` de `rx.vstack`/`rx.hstack`: nos mesmos artefatos esse caso aparece como prop `gap:"4"` do Radix, que usa sua escala de espaçamento. Não deve ser substituído indiscriminadamente.

### Pontos ainda sem evidência suficiente

- Os selects de abertura de chamado e atendimento não têm altura explícita de 48 px; o estilo global define altura apenas para `rx.input`. O componente instalado documenta tamanho padrão `2`, mas a altura efetiva ainda precisa ser medida. Portanto, a divergência de altura permanece pendente de confirmação visual.
- Badges usam esquemas Radix e padding próprios, enquanto os frames usam cores suaves e altura de 28 px. Sem estilos computados no navegador, não é possível aprovar equivalência exata das cores e dimensões.
- Login, dashboards, listas/detalhes de tarefas, telas específicas do gestor, edição e logs continuam sem contexto completo local dos respectivos frames. Não atribuir a essas telas medidas de outro frame como se fossem requisitos confirmados.

Nesta continuação foi modificado apenas este relatório. Nenhum componente, regra de negócio, endpoint ou dado remoto foi alterado. Não foram executados testes funcionais nem compilação.
