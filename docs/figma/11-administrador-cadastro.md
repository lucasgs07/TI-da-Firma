# Referência Figma — 11-administrador-cadastro

Consultada em 21/10/2026. Frame `5:343`.

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=5-343

Contexto completo retornado pelo conector; a screenshot também foi recebida e inspecionada nesta consulta. Código de referência em React/Tailwind, a ser traduzido para Reflex. Os exemplos de dados não são registros reais.

```text
function NavigationItem({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] w-[200px]"} data-node-id="2:57" data-name="Navigation/Item">
      <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="2:58">
        Chamados
      </p>
    </div>
  );
}

export default function Component11AdministradorCadastrarUsuario() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="5:343" data-name="11 · Administrador · Cadastrar usuário">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="5:344" data-name="Navegação · Administrador">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:345" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="5:346">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:347">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="5:348">
          ÁREA DO ADMINISTRADOR
        </p>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:349" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:349;2:58">
            Dashboard
          </p>
        </div>
        <NavigationItem className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" />
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:353" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:353;2:58">
            Tarefas
          </p>
        </div>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:355" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:355;2:58">
            Usuários
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:357" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:357;2:58">
            Logs
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="5:359" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:360" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="5:361">
            Douglas Lobo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:362">
            Administrador · T.I.
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:363">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="5:364" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="5:365" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="5:366">{`Workspace  /  Usuários`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="5:367" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:368">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="5:369">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="5:370" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:371" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:372" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:373">
                Uma nova pessoa na firma.
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px]" data-node-id="5:374">
                Cadastre o usuário e defina seu perfil de acesso.
              </p>
            </div>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="5:375" data-name="Cadastro e permissões">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[744px]" data-node-id="5:376" data-name="Dados do novo usuário">
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:377" data-name="Nome *">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:378">
                  Nome *
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="5:379" data-name="Input/Default">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:379;2:56">
                    Ana Souza
                  </p>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:381" data-name="E-mail *">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:382">
                  E-mail *
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="5:383" data-name="Input/Default">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:383;2:56">
                    ana.souza@empresa.com.br
                  </p>
                </div>
              </div>
              <div className="content-stretch flex gap-[var(--ti-space-16,16px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:385" data-name="Perfil e departamento">
                <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[340px]" data-node-id="5:386" data-name="Perfil *">
                  <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:387">
                    Perfil *
                  </p>
                  <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[340px]" data-node-id="5:388" data-name="Input/Default">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:388;2:56">
                      Técnico
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[340px]" data-node-id="5:390" data-name="Departamento *">
                  <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:391">
                    Departamento *
                  </p>
                  <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[340px]" data-node-id="5:392" data-name="Input/Default">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:392;2:56">
                      T.I. · obrigatório para técnicos
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:394" data-name="Senha inicial *">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:395">
                  Senha inicial *
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="5:396" data-name="Input/Default">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:396;2:56">
                    ••••••••••••
                  </p>
                </div>
              </div>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:398">
                Pelo menos 8 caracteres, uma letra e um número.
              </p>
              <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:399" data-name="Button/Primary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:399;2:38">
                  Cadastrar usuário
                </p>
              </div>
            </div>
            <div className="[word-break:break-word] bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start not-italic overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[360px]" data-node-id="5:401" data-name="Orientações de acesso">
              <p className="font-['Inter:Semi_Bold'] font-semibold leading-[1.45] relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:402">
                Cada pessoa, sua área.
              </p>
              <div className="font-['Inter:Regular'] font-normal h-[224px] leading-[0] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[312px] whitespace-pre-wrap" data-node-id="5:403">
                <p className="leading-[1.45] mb-0">Funcionário</p>
                <p className="leading-[1.45] mb-0">Abre chamados e conclui tarefas próprias.</p>
                <p className="leading-[1.45] mb-0">​</p>
                <p className="leading-[1.45] mb-0">Técnico</p>
                <p className="leading-[1.45] mb-0">Participa do atendimento.</p>
                <p className="leading-[1.45] mb-0">​</p>
                <p className="leading-[1.45] mb-0">Gestor</p>
                <p className="leading-[1.45] mb-0">Organiza demandas do seu escopo.</p>
                <p className="leading-[1.45] mb-0">​</p>
                <p className="leading-[1.45] mb-0">Administrador</p>
                <p className="leading-[1.45]">Consulta global e gerencia usuários.</p>
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
```

```text
The generated code contains image and SVG URL constants, e.g. const image = `${assetPathPrefix}/<asset file name>`, where assetPathPrefix is declared once at the top of the code and every asset URL interpolates it. These URLs are temporary download sources and expire after 7 days. Download each asset into the project with curl -L, then replace its URL in the generated code with a reference to the downloaded asset. Never use the temporary URLs as runtime image sources.
```
