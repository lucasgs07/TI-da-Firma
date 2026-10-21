# Referência Figma — frame 5:279

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=5-279

Contexto consultado em 21/10/2026 para revisão. Exemplos do design não são dados reais. Imagem retornada pelo conector; comparação com a aplicação renderizada permanece pendente.

```tsx
function NavigationItem({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] w-[200px]"} data-node-id="2:57" data-name="Navigation/Item">
      <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="2:58">
        Chamados
      </p>
    </div>
  );
}

export default function Component10GestorNovaTarefa() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="5:279" data-name="10 · Gestor · Nova tarefa">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="5:280" data-name="Navegação · Gestor">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:281" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="5:282">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:283">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="5:284">
          ÁREA DO GESTOR
        </p>
        <NavigationItem className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" />
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:287" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:287;2:58">
            Abrir chamado
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:289" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:289;2:58">
            Cadastrar usuário
          </p>
        </div>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:291" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:291;2:58">
            Nova tarefa
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="5:293" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:294" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="5:295">
            Camila Santos
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:296">
            Gestor · Financeiro
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:297">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="5:298" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="5:299" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="5:300">{`Workspace  /  Nova tarefa`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="5:301" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:302">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="5:303">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="5:304" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:305" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:306" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:307">
                Transforme uma demanda em ação.
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px]" data-node-id="5:308">
                Atribua a tarefa a um ou mais funcionários do seu departamento.
              </p>
            </div>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="5:309" data-name="Criação de tarefa">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[744px]" data-node-id="5:310" data-name="Formulário da tarefa">
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:311" data-name="Título *">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:312">
                  Título *
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="5:313" data-name="Input/Default">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:313;2:56">
                    Validar impressora do setor
                  </p>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:315" data-name="Descrição">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:316">
                  Descrição
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[112px] items-start pl-[14px] pt-[14px] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="5:317" data-name="Input/Default">
                  <p className="[word-break:break-word] flex-[1_0_0] font-['Inter:Regular'] font-normal leading-[1.45] min-w-px not-italic relative text-[14px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:317;2:56">
                    Realizar teste de impressão após a manutenção.
                  </p>
                </div>
              </div>
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:319">
                Responsáveis *
              </p>
              <div className="[word-break:break-word] bg-[var(--ti-bg,#f4f7f6)] content-stretch flex font-['Inter:Regular'] font-normal gap-[var(--ti-space-24,24px)] h-[48px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[696px] whitespace-pre" data-node-id="5:320" data-name="Seleção múltipla">
                <p className="relative shrink-0" data-node-id="5:321">{`☑  Marina Costa`}</p>
                <p className="relative shrink-0" data-node-id="5:322">{`☑  Carlos Oliveira`}</p>
              </div>
              <div className="content-stretch flex gap-[var(--ti-space-16,16px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:323" data-name="Prioridade e prazo">
                <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[340px]" data-node-id="5:324" data-name="Prioridade *">
                  <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:325">
                    Prioridade *
                  </p>
                  <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[340px]" data-node-id="5:326" data-name="Input/Default">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:326;2:56">
                      Alta
                    </p>
                  </div>
                </div>
                <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[340px]" data-node-id="5:328" data-name="Prazo · opcional">
                  <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:329">
                    Prazo · opcional
                  </p>
                  <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[340px]" data-node-id="5:330" data-name="Input/Default">
                    <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:330;2:56">
                      21/10/2026
                    </p>
                  </div>
                </div>
              </div>
              <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[696px]" data-node-id="5:332" data-name="Nº do chamado · opcional">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:333">
                  Nº do chamado · opcional
                </p>
                <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[696px]" data-node-id="5:334" data-name="Input/Default">
                  <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:334;2:56">
                    1048
                  </p>
                </div>
              </div>
              <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[160px]" data-node-id="5:336" data-name="Button/Primary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:336;2:38">
                  Criar tarefa
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[360px]" data-node-id="5:338" data-name="Regras de atribuição">
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:339">
                Trabalho compartilhado
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[61px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[312px]" data-node-id="5:340">
                Qualquer responsável pode concluir a tarefa inteira, informando uma única solução.
              </p>
              <div className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex gap-[var(--ti-space-12,12px)] items-start overflow-clip p-[var(--ti-space-16,16px)] relative rounded-[8px] shrink-0 w-[312px]" data-node-id="5:341" data-name="Orientação">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[61px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] w-[280px]" data-node-id="5:342">
                  Você pode selecionar funcionários do Financeiro. O gestor de T.I. seleciona técnicos de T.I.
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

