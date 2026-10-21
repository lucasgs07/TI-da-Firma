# Referência Figma — 06-tecnico-atendimento

Consultada em 21/10/2026. Frame `3:347`.

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=3-347

Contexto completo retornado pelo conector; a screenshot também foi recebida e inspecionada nesta consulta. Código de referência em React/Tailwind, a ser traduzido para Reflex. Os exemplos de dados não são registros reais.

```text
function BadgeEmAtendimento({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:45" data-name="Badge/Em atendimento">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-amber,#9b600c)] whitespace-nowrap" data-node-id="2:46">
        Em atendimento
      </p>
    </div>
  );
}

export default function Component06TecnicoAtendimento() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="3:347" data-name="06 · Técnico · Atendimento">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="3:348" data-name="Navegação · Técnico">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:349" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="3:350">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:351">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="3:352">
          ÁREA DO TÉCNICO
        </p>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:353" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:353;2:58">
            Todos os chamados
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:355" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I3:355;2:58">
            Minhas tarefas
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="3:357" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:358" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="3:359">
            Lucas Gomes
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:360">
            Técnico · T.I.
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:361">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="3:362" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="3:363" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="3:364">{`Workspace  /  Todos os chamados`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="3:365" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:366">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="3:367">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="3:368" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="3:369" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="3:370" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:371">
                Impressora do financeiro offline
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px] whitespace-pre-wrap" data-node-id="3:372">{`Todos os chamados  /  #1048  ·  Marina Costa · Financeiro`}</p>
            </div>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="3:373" data-name="Atendimento e contexto">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[744px]" data-node-id="3:374" data-name="Histórico e comentário">
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:375">
                Histórico do atendimento
              </p>
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:376">
                Marina Costa · 21 out, 09:10 (UTC−03:00)
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[696px]" data-node-id="3:377">
                A impressora aparece offline. Reiniciei, mas o problema continua.
              </p>
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:378">
                Lucas Gomes · 21 out, 14:32 (UTC−03:00)
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[696px]" data-node-id="3:379">
                Identifiquei uma falha na configuração de rede. Vou ajustar a conexão e validar a impressão com o setor.
              </p>
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="3:380" data-name="Adicionar comentário">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:381">
                  Adicionar comentário
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[112px] items-start pl-[14px] pt-[14px] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="3:382" data-name="Input/Default">
                  <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[1.45] min-w-px not-italic relative text-[14px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:382;2:56">
                    Escreva uma atualização para o histórico…
                  </p>
                </div>
              </div>
              <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[190px]" data-node-id="3:384" data-name="Button/Primary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:384;2:38">
                  Enviar comentário
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[360px]" data-node-id="3:386" data-name="Painel de atendimento">
              <BadgeEmAtendimento className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[120px]" />
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:389">
                Técnicos associados
              </p>
              <div className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[0] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:390">
                <p className="leading-[1.45] mb-0">Lucas Gomes · você</p>
                <p className="leading-[1.45]">Pedro Lima</p>
              </div>
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[312px]" data-node-id="3:391" data-name="Status">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:392">
                  Status
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[312px]" data-node-id="3:393" data-name="Input/Default">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I3:393;2:56">
                    Em atendimento
                  </p>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[312px]" data-node-id="3:395" data-name="Solução final">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:396">
                  Solução final
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[112px] items-start pl-[14px] pt-[14px] relative rounded-[8px] shrink-0 w-[312px]" data-node-id="3:397" data-name="Input/Default">
                  <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[1.45] min-w-px not-italic relative text-[14px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:397;2:56">
                    Descreva a solução aplicada…
                  </p>
                </div>
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[18px] leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] w-[312px]" data-node-id="3:399">
                Obrigatória para resolver ou fechar o chamado.
              </p>
              <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[312px]" data-node-id="3:400" data-name="Button/Primary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:400;2:38">
                  Salvar atendimento
                </p>
              </div>
              <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[312px]" data-node-id="3:402" data-name="Button/Secondary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I3:402;2:40">
                  Resolver chamado
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

## Button/Primary
**Node ID:** 2:37

Ação reutilizável de 44px. Texto ajustável por instância.

## Button/Secondary
**Node ID:** 2:39

Ação reutilizável de 44px. Texto ajustável por instância.
```

```text
The generated code contains image and SVG URL constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These URLs are temporary download sources and expire after 7 days. Download each asset into the project with curl -L, then replace its URL in the generated code with a reference to the downloaded asset. Never use the temporary URLs as runtime image sources.
```
