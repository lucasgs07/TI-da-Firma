# Referência Figma — 16-estados-interface

Consultada em 21/10/2026. Frame `6:196`.

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=6-196

Contexto completo retornado pelo conector; a screenshot também foi recebida e inspecionada nesta consulta. Código de referência em React/Tailwind, a ser traduzido para Reflex. Os exemplos de dados não são registros reais.

```text
export default function Component16EstadosDeInterface() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start p-[var(--ti-space-40,40px)] relative size-full" data-node-id="6:196" data-name="16 · Estados de interface">
      <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="6:197">
        Cada estado orienta o próximo passo.
      </p>
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="6:198">
        Comportamentos previstos para implementação · exemplos com dados fictícios
      </p>
      <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-start overflow-clip relative shrink-0 w-[1360px]" data-node-id="6:199" data-name="Estados">
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[437px]" data-node-id="6:200" data-name="Nenhum chamado por aqui">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[27px] leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] w-[389px]" data-node-id="6:201">
            Nenhum chamado por aqui
          </p>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[389px]" data-node-id="6:202">
            Quando precisar da equipe de T.I., abra sua primeira solicitação.
          </p>
          <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[220px]" data-node-id="6:203" data-name="Button/Primary">
            <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I6:203;2:38">
              Abrir chamado
            </p>
          </div>
        </div>
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[437px]" data-node-id="6:205" data-name="Não foi possível carregar">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[27px] leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] w-[389px]" data-node-id="6:206">
            Não foi possível carregar
          </p>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[389px]" data-node-id="6:207">
            Confira sua conexão e tente novamente. Seus dados preenchidos serão mantidos.
          </p>
          <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[220px]" data-node-id="6:208" data-name="Button/Primary">
            <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I6:208;2:38">
              Tentar novamente
            </p>
          </div>
        </div>
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[437px]" data-node-id="6:210" data-name="Chamado criado!">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[27px] leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] w-[389px]" data-node-id="6:211">
            Chamado criado!
          </p>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[389px]" data-node-id="6:212">
            Sua solicitação #1053 foi registrada. Acompanhe o atendimento na sua lista.
          </p>
          <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[220px]" data-node-id="6:213" data-name="Button/Primary">
            <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I6:213;2:38">
              Ver meus chamados
            </p>
          </div>
        </div>
      </div>
      <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-start overflow-clip relative shrink-0 w-[1360px]" data-node-id="6:215" data-name="Validação e carregamento">
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[660px]" data-node-id="6:216" data-name="Campos obrigatórios">
          <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[612px]" data-node-id="6:217" data-name="Título *">
            <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="6:218">
              Título *
            </p>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[612px]" data-node-id="6:219" data-name="Input/Default">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I6:219;2:56">
                Digite um título para o chamado
              </p>
            </div>
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-red,#b64040)] whitespace-nowrap" data-node-id="6:221">
            Informe o título antes de enviar.
          </p>
          <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[220px]" data-node-id="6:222" data-name="Button/Primary">
            <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I6:222;2:38">
              Enviar chamado
            </p>
          </div>
        </div>
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[676px]" data-node-id="6:224" data-name="Carregamento">
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="6:225">
            Carregando seus chamados…
          </p>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="6:226">
            Aguarde enquanto buscamos suas solicitações.
          </p>
          <div className="bg-[var(--ti-border,#dfe7e4)] h-[16px] relative rounded-[8px] shrink-0 w-[580px]" data-node-id="6:227" data-name="Skeleton" />
          <div className="bg-[var(--ti-border,#dfe7e4)] h-[16px] relative rounded-[8px] shrink-0 w-[430px]" data-node-id="6:228" data-name="Skeleton" />
          <div className="bg-[var(--ti-border,#dfe7e4)] h-[16px] relative rounded-[8px] shrink-0 w-[500px]" data-node-id="6:229" data-name="Skeleton" />
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
These styles are contained in the design: TI/Title: Font(family: "Inter", style: Semi Bold, size: 28, weight: 600, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Body: Font(family: "Inter", style: Regular, size: 14, weight: 400, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Heading: Font(family: "Inter", style: Semi Bold, size: 18, weight: 600, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Label: Font(family: "Inter", style: Medium, size: 14, weight: 500, lineHeight: 1.4500000476837158, letterSpacing: 0), TI/Caption: Font(family: "Inter", style: Regular, size: 12, weight: 400, lineHeight: 1.4500000476837158, letterSpacing: 0).
```

```text
Component descriptions: The following components have usage descriptions or documentation links defined in Figma. These descriptions provide important context about the intended usage, best practices, and any constraints for each component. Follow these guidelines when implementing or using these components.

## Button/Primary
**Node ID:** 2:37

Ação reutilizável de 44px. Texto ajustável por instância.
```

```text
The generated code contains image and SVG URL constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These URLs are temporary download sources and expire after 7 days. Download each asset into the project with curl -L, then replace its URL in the generated code with a reference to the downloaded asset. Never use the temporary URLs as runtime image sources.
```
