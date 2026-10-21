# Aplicação do design Nexo

Referência: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j (página `0:1`).

## Escopo

Aplicar a identidade visual e os layouts obtidos do Figma aos fluxos existentes em Reflex, sem alterar contratos, regras de autorização ou o ambiente Xano. As especificações existentes de autenticação, chamados e tarefas continuam válidas. Os registros demonstrativos do Figma não devem substituir dados da API.

## Decisões

- Componentes compartilhados para navegação, títulos, métricas, tabelas, formulários e badges; verde `#16765b`, navegação `#142d29`, fundo `#f4f7f6`, bordas `#dfe7e4` e tipografia Inter.
- Sidebar de 232px e barra superior de 72px no desktop; menu acessível e cartões de chamados no celular.
- Busca e filtros operam somente sobre os registros já autorizados e retornados pela API.
- Não exibir datas fictícias. A lista do funcionário usa categoria no lugar da coluna de atualização, pois seu contrato atual não fornece essa data.
- A lista de tarefas usa status no lugar de prioridade: o contrato público de tarefas disponível contém o ID da prioridade, sem seu nome. O histórico preserva a data formatada pelo cliente existente e identifica UTC; não aplica silenciosamente o fuso dos exemplos do Figma.
- Contagens calculadas sobre listas são identificadas como registros carregados; indicadores globais administrativos continuam vindos do endpoint existente.
- Falhas de consulta continuam distintas de listas vazias e formulários preservam os eventos e as validações existentes.

## Consulta das referências

Na primeira leitura, o conector Figma atingiu o limite do plano Starter. Em nova consulta de 21/10/2026, as cinco referências restantes foram recuperadas com contexto completo e screenshots. A consulta das telas está concluída; a adaptação específica dessas referências ao código e sua validação visual continuam pendentes.

| Frame | Tela | Referência local |
| --- | --- | --- |
| `3:192` | Funcionário · Detalhe do chamado | [Contexto](figma/04-funcionario-detalhe.md) |
| `3:347` | Técnico · Atendimento | [Contexto](figma/06-tecnico-atendimento.md) |
| `5:343` | Administrador · Cadastrar usuário | [Contexto](figma/11-administrador-cadastro.md) |
| `6:169` | Mobile · Abrir chamado | [Contexto](figma/15-mobile-abrir-chamado.md) |
| `6:196` | Estados de interface | [Contexto](figma/16-estados-interface.md) |

### Achados para a próxima adaptação

- **Detalhe do funcionário:** relato à esquerda (744px), resumo à direita (360px), intervalo de 24px; badge de status, categoria, prioridade e retorno à lista. O design mostra datas de abertura/atualização e departamento do solicitante que não estão no contrato público atual do funcionário; não preencher com exemplos fictícios.
- **Atendimento técnico:** histórico e comentário à esquerda (744px), painel de atendimento à direita (360px). O painel contém técnicos associados, status, solução final, salvar e resolver. O botão de resolver deverá reutilizar o fluxo autorizado existente, mantendo solução obrigatória e as verificações de associação. Os horários exemplificam UTC−03:00; a apresentação atual do cliente usa UTC.
- **Cadastro administrativo:** título “Uma nova pessoa na firma.”; formulário com nome, e-mail, perfil/departamento lado a lado e senha inicial ao final. Card lateral “Cada pessoa, sua área.” descreve os quatro perfis. A vinculação de técnicos a T.I. permanece obrigatória; a regra da senha segue a validação existente.
- **Abrir chamado mobile:** frame de 390×844px, cabeçalho de 72px, margens de 20px, conteúdo de 350px. Campos em coluna, inputs de 48px, descrição de 112px e botões de 44px ocupando toda a largura. O formulário fica diretamente sobre o fundo, sem o card e o painel de dicas do desktop.
- **Estados:** vazio com ação de abrir; erro com nova tentativa e preservação dos dados; sucesso com retorno à lista; mensagem de validação abaixo do campo; carregamento com três skeletons de 16px. Os textos e IDs são exemplos, não evidências de operações reais.

Esta nova consulta modificou apenas documentação e referências locais. Nenhum componente, evento ou endpoint foi alterado nesta etapa.

## Critérios de verificação

- Compilação Reflex e testes existentes dos quatro perfis sem regressão.
- Navegação por perfil, logout e rotas protegidas preservados.
- Nenhum dado demonstrativo apresentado como dado real; nenhum endpoint ou schema modificado.
- Conferência visual de login e layout responsivo; fluxos autenticados reais dependem de sessão disponível.

## Arquivos da implementação

Criados: `TI_da_Firma/design.py`, `TI_da_Firma/shell.py`, `assets/nexo.css` e este documento.

Modificados: `TI_da_Firma/TI_da_Firma.py`, `TI_da_Firma/technician_portal.py`, `TI_da_Firma/office_portal.py`, `TI_da_Firma/admin_portal.py`, `TI_da_Firma/auth_state.py`, `TI_da_Firma/office_state.py` e `rxconfig.py`.

A fonte Inter é carregada do Google Fonts pelo CSS, com fallback sans-serif. Não há imagens ou SVGs estáticos nos contextos implementados; a referência visual não foi usada como imagem da interface.

## Verificações realizadas em 21/10/2026

- `python -m pytest tests -q -p no:cacheprovider`: 141 testes passaram.
- `reflex compile --dry`: compilação concluída.
- `reflex run --env prod --single-port`: build de produção concluído e aplicação local iniciada na porta 3000.
- GET `/login` e `/nexo.css`: HTTP 200.
- Verificação local de busca sem distinção de maiúsculas/minúsculas, combinação de filtros, escolha da lista por perfil, limpeza dos filtros na sessão e resumo de tarefas: passou.
- Não foi possível inspecionar o resultado renderizado: o inventário de automação retornou nenhum navegador disponível. Responsividade e comparação visual com os frames permanecem sem validação no navegador.
- Nenhum teste autenticado remoto ou operação de gravação no Xano foi executado nesta alteração.

## Atualização por imagens fornecidas em 21/10/2026

Após o limite do conector Figma, o usuário enviou seis imagens como referência: diretório e edição administrativos e pesquisa de chamados dos quatro perfis. A adaptação usa essas imagens diretamente como referência visual, sem inserir screenshots nem registros demonstrativos na interface.

- Diretório: título, contagem real, linhas alternadas, status com badge e ações de edição/paginação.
- Edição: seções Dados pessoais e Acesso ao sistema, campos em duas colunas no desktop e resumo lateral do cadastro carregado. O resumo corresponde aos dados carregados; alterações ainda não salvas permanecem nos controles do formulário.
- Pesquisa: painel com rótulos, instrução, campos em grade responsiva e ações Aplicar/Limpar. Contagens usam os registros carregados, respeitando o escopo.
- O campo Solicitante permanece disponível ao funcionário conforme o requisito aprovado, embora omitido na imagem desse perfil. Sua coluna usa o nome da sessão, pois todos os registros autorizados desse perfil são próprios.
- Os atalhos existentes de abertura/atualização e as permissões gerenciais de T.I. foram preservados.
- Nenhuma alteração de endpoint, banco, credenciais ou publicação remota nesta adaptação.

Arquivos modificados nesta etapa: admin_portal.py, ticket_filters.py, design.py, TI_da_Firma.py, technician_portal.py, office_portal.py, assets/nexo.css e este documento.
Validação: 178 testes Python passaram; compilação Reflex concluída. A comparação renderizada no navegador permanece pendente.
