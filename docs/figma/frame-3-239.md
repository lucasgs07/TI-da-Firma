# Referência Figma — frame 3:239

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=3-239

Contexto consultado em 21/10/2026 para revisão. Exemplos do design não são dados reais. Imagem retornada pelo conector; comparação com a aplicação renderizada permanece pendente.

```tsx
function BadgeMedia({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:51" data-name="Badge/Média">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-amber,#9b600c)] whitespace-nowrap" data-node-id="2:52">
        Média
      </p>
    </div>
  );
}

function BadgeResolvido({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:47" data-name="Badge/Resolvido">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="2:48">
        Resolvido
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

function BadgeAberto({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-blueSoft,#eaf1fc)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:43" data-name="Badge/Aberto">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-blue,#275eaa)] whitespace-nowrap" data-node-id="2:44">
        Aberto
      </p>
    </div>
  );
}

function BadgeAlta({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:49" data-name="Badge/Alta">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-red,#b64040)] whitespace-nowrap" data-node-id="2:50">
        Alta
      </p>
    </div>
  );
}

export default function Component05TecnicoFilaDeChamados() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="3:239" data-name="05 · Técnico · Fila de chamados">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="3:240" data-name="Navegação · Técnico">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:241" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="3:242">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:243">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="3:244">
          ÁREA DO TÉCNICO
        </p>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:245" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:245;2:58">
            Todos os chamados
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:247" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I3:247;2:58">
            Minhas tarefas
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="3:249" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:250" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="3:251">
            Lucas Gomes
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:252">
            Técnico · T.I.
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:253">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="3:254" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="3:255" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="3:256">{`Workspace  /  Todos os chamados`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="3:257" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:258">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="3:259">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="3:260" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="3:261" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="3:262" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:263">
                Tudo pronto para resolver.
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px]" data-node-id="3:264">
                Consulte os chamados e associe-se aos que precisam de você.
              </p>
            </div>
          </div>
          <div className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex gap-[var(--ti-space-12,12px)] items-start overflow-clip p-[var(--ti-space-16,16px)] relative rounded-[8px] shrink-0 w-[1128px]" data-node-id="3:265" data-name="Orientação">
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] w-[1096px]" data-node-id="3:266">
              Há 6 chamados abertos aguardando associação.
            </p>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[48px] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="3:267" data-name="Filtros da fila">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[560px]" data-node-id="3:268" data-name="Input/Default">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I3:268;2:56">
                Buscar por número ou título…
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[220px]" data-node-id="3:270" data-name="Button/Secondary">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I3:270;2:40">
                Todos os status
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[180px]" data-node-id="3:272" data-name="Button/Secondary">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I3:272;2:40">
                Prioridade
              </p>
            </div>
          </div>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[12px] shrink-0 w-[1128px]" data-node-id="3:274" data-name="Tabela">
            <div className="[word-break:break-word] bg-[var(--ti-bg,#f4f7f6)] content-stretch flex font-['Inter:Regular'] font-normal h-[48px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] w-[1128px]" data-node-id="3:275" data-name="Cabeçalho da tabela">
              <p className="h-[18px] relative shrink-0 w-[80px]" data-node-id="3:276">
                Nº
              </p>
              <p className="h-[18px] relative shrink-0 w-[380px]" data-node-id="3:277">
                Solicitação
              </p>
              <p className="h-[18px] relative shrink-0 w-[200px]" data-node-id="3:278">
                Status
              </p>
              <p className="h-[18px] relative shrink-0 w-[150px]" data-node-id="3:279">
                Prioridade
              </p>
              <p className="h-[18px] relative shrink-0 w-[286px]" data-node-id="3:280">
                Técnicos
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:281" data-name="Linha · #1052">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:282" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:283">
                  #1052
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:284" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:285">
                  Sem acesso ao sistema financeiro
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:286" data-name="Célula">
                <BadgeAberto className="bg-[var(--ti-blueSoft,#eaf1fc)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:289" data-name="Célula">
                <BadgeAlta className="bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:292" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:293">
                  Sem técnicos
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:294" data-name="Linha · #1048">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:295" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:296">
                  #1048
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:297" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:298">
                  Impressora do financeiro offline
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:299" data-name="Célula">
                <BadgeEmAtendimento className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[120px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:302" data-name="Célula">
                <BadgeAlta className="bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:305" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:306">
                  Lucas, Pedro
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:307" data-name="Linha · #1046">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:308" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:309">
                  #1046
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:310" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:311">
                  Acesso à pasta compartilhada
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:312" data-name="Célula">
                <BadgeAberto className="bg-[var(--ti-blueSoft,#eaf1fc)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:315" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:318" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:319">
                  Sem técnicos
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:320" data-name="Linha · #1043">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:321" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:322">
                  #1043
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:323" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:324">
                  Computador reiniciando
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:325" data-name="Célula">
                <BadgeEmAtendimento className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[120px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:328" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:331" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:332">
                  Ana Souza
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:333" data-name="Linha · #1030">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:334" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:335">
                  #1030
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:336" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:337">
                  Problema ao conectar ao Wi-Fi
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:338" data-name="Célula">
                <BadgeResolvido className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[85px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:341" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:344" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:345">
                  Lucas Gomes
                </p>
              </div>
            </div>
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:346">
            Abra um chamado para consultar o histórico ou participar do atendimento.
          </p>
        </div>
      </div>
    </div>
  );
}
```

