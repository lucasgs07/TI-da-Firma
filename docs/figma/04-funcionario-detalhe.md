# Referência Figma — 04-funcionario-detalhe

Consultada em 21/10/2026. Frame `3:192`.

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=3-192

Contexto completo retornado pelo conector; a screenshot também foi recebida e inspecionada nesta consulta. Código de referência em React/Tailwind, a ser traduzido para Reflex. Os exemplos de dados não são registros reais.

```text
function BadgeAlta({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:49" data-name="Badge/Alta">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-red,#b64040)] whitespace-nowrap" data-node-id="2:50">
        Alta
      </p>
    </div>
  );
}

function BadgeEmAtendimento({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:45" data-name="Badge/Em atendimento">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-amber,#9b600c)] whitespace-nowrap" data-node-id="2:46">
        Em atendimento
      </p>
    </div>
  );
}

export default function Component04FuncionarioDetalheDoChamado() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="3:192" data-name="04 · Funcionário · Detalhe do chamado">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="3:193" data-name="Navegação · Funcionário">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:194" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="3:195">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:196">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="3:197">
          ÁREA DO FUNCIONÁRIO
        </p>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:198" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:198;2:58">
            Meus chamados
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:200" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I3:200;2:58">
            Minhas tarefas
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="3:202" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:203" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="3:204">
            Marina Costa
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:205">
            Funcionário · Financeiro
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:206">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="3:207" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="3:208" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="3:209">{`Workspace  /  Meus chamados`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="3:210" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:211">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="3:212">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="3:213" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="3:214" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="3:215" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:216">
                Impressora do financeiro offline
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px] whitespace-pre-wrap" data-node-id="3:217">{`Meus chamados  /  #1048`}</p>
            </div>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="3:218" data-name="Detalhes">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[744px]" data-node-id="3:219" data-name="Relato">
              <BadgeEmAtendimento className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[120px]" />
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:222">
                Descrição da solicitação
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[696px]" data-node-id="3:223">
                A impressora do financeiro aparece como offline desde hoje pela manhã. Já reiniciei o equipamento, mas ainda não consigo imprimir os relatórios.
              </p>
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:224">
                Informações do chamado
              </p>
              <div className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[0] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[696px]" data-node-id="3:225">
                <p className="leading-[1.45] mb-0">Aberto em 21/10/2026 às 09:10 (UTC−03:00)</p>
                <p className="leading-[1.45]">Última atualização: hoje às 14:32 (UTC−03:00)</p>
              </div>
              <div className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex gap-[var(--ti-space-12,12px)] items-start overflow-clip p-[var(--ti-space-16,16px)] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="3:226" data-name="Orientação">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] w-[664px]" data-node-id="3:227">
                  Sua solicitação está em atendimento pela equipe de T.I.
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[360px]" data-node-id="3:228" data-name="Classificação">
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:229">
                Resumo do chamado
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:230">
                Categoria
              </p>
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:231">
                Hardware
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:232">
                Prioridade
              </p>
              <BadgeAlta className="bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:235">
                Solicitante
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:236">
                Marina Costa · Financeiro
              </p>
              <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[312px]" data-node-id="3:237" data-name="Button/Secondary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I3:237;2:40">
                  Voltar aos chamados
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
```

```text
SUPER CRITICAL: The generated React+Tailwind code MUST be converted to match the target project's technology stack and styling system.
1. Analyze the target codebase to identify: technology stack, styling approach, component patterns, and design tokens
2. Convert React syntax to the target framework/library
3. Transform all Tailwind classes to the target styling system while preserving exact visual design
4. Follow the project's existing patterns and conventions
DO NOT install any Tailwind as a dependency unless the user instructs you to do so.

```

```text
Node ids have been added to the code as data attributes, e.g. `data-node-id="1:2"`.
```

```text
These styles are contained in the design: TI/Heading: Font(family: "Inter", style: Semi Bold, size: 18, weight: 600, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Caption: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Label: Font(family: "Inter", style: Medium, size: 14, weight: 500, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Title: Font(family: "Inter", style: Semi Bold, size: 28, weight: 600, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Body: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 1.4500000476837158, letterSpacing: 0).
```

```text
Component descriptions: The following components have usage descriptions or documentation links defined in Figma. These descriptions provide important context about the intended usage, best practices, and any constraints for each component. Follow these guidelines when implementing or using these components.

## Button/Secondary
**Node ID:** 2:39

Ação reutilizável de 44px. Texto ajustável por instância.
```

```text
The generated code contains image and SVG URL constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These URLs are temporary download sources and expire after 7 days. Download each asset into the project with curl -L, then replace its URL in the generated code with a reference to the downloaded asset. Never use the temporary URLs as runtime image sources.
```
