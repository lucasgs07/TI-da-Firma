# Referência Figma — frame 3:30

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=3-30

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

function BadgeBaixa({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:53" data-name="Badge/Baixa">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="2:54">
        Baixa
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

function BadgeEmAtendimento({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:45" data-name="Badge/Em atendimento">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-amber,#9b600c)] whitespace-nowrap" data-node-id="2:46">
        Em atendimento
      </p>
    </div>
  );
}

export default function Component02FuncionarioMeusChamados() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="3:30" data-name="02 · Funcionário · Meus chamados">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="3:31" data-name="Navegação · Funcionário">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:32" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="3:33">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:34">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="3:35">
          ÁREA DO FUNCIONÁRIO
        </p>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:36" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:36;2:58">
            Meus chamados
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:38" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I3:38;2:58">
            Minhas tarefas
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="3:40" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="3:41" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="3:42">
            Marina Costa
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:43">
            Funcionário · Financeiro
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="3:44">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="3:45" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="3:46" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="3:47">{`Workspace  /  Meus chamados`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="3:48" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:49">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="3:50">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="3:51" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1124px]" data-node-id="3:52" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[900px]" data-node-id="3:53" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:54">
                Como podemos ajudar, Marina?
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[850px]" data-node-id="3:55">
                Acompanhe suas solicitações e fale com a equipe de T.I.
              </p>
            </div>
            <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[200px]" data-node-id="3:56" data-name="Button/Primary">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:56;2:38">
                + Abrir chamado
              </p>
            </div>
          </div>
          <div className="[word-break:break-word] content-stretch flex gap-[var(--ti-space-16,16px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1128px] whitespace-nowrap" data-node-id="3:58" data-name="Indicadores">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[365.333px]" data-node-id="3:59" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:59;2:60">
                Abertos
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I3:59;2:61">
                02
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:59;2:62">
                Aguardando atendimento
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[365.333px]" data-node-id="3:63" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:63;2:60">
                Em atendimento
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I3:63;2:61">
                01
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:63;2:62">
                Equipe trabalhando
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[365.333px]" data-node-id="3:67" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:67;2:60">
                Resolvidos
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I3:67;2:61">
                08
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I3:67;2:62">
                Solicitações concluídas
              </p>
            </div>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[48px] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="3:71" data-name="Busca e filtros">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[640px]" data-node-id="3:72" data-name="Input/Default">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I3:72;2:56">
                Buscar nos meus chamados…
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[220px]" data-node-id="3:74" data-name="Button/Secondary">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I3:74;2:40">
                Todos os status
              </p>
            </div>
          </div>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[12px] shrink-0 w-[1128px]" data-node-id="3:76" data-name="Tabela">
            <div className="[word-break:break-word] bg-[var(--ti-bg,#f4f7f6)] content-stretch flex font-['Inter:Regular'] font-normal h-[48px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] w-[1128px]" data-node-id="3:77" data-name="Cabeçalho da tabela">
              <p className="h-[18px] relative shrink-0 w-[80px]" data-node-id="3:78">
                Nº
              </p>
              <p className="h-[18px] relative shrink-0 w-[380px]" data-node-id="3:79">
                Solicitação
              </p>
              <p className="h-[18px] relative shrink-0 w-[200px]" data-node-id="3:80">
                Status
              </p>
              <p className="h-[18px] relative shrink-0 w-[150px]" data-node-id="3:81">
                Prioridade
              </p>
              <p className="h-[18px] relative shrink-0 w-[286px]" data-node-id="3:82">
                Atualizado
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:83" data-name="Linha · #1048">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:84" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:85">
                  #1048
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:86" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:87">
                  Impressora do financeiro offline
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:88" data-name="Célula">
                <BadgeEmAtendimento className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[120px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:91" data-name="Célula">
                <BadgeAlta className="bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:94" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:95">
                  Hoje, 14:32
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:96" data-name="Linha · #1046">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:97" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:98">
                  #1046
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:99" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:100">
                  Acesso à pasta compartilhada
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:101" data-name="Célula">
                <BadgeAberto className="bg-[var(--ti-blueSoft,#eaf1fc)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:104" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:107" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:108">
                  Hoje, 10:15
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:109" data-name="Linha · #1041">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:110" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:111">
                  #1041
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:112" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:113">
                  Instalação do Microsoft Teams
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:114" data-name="Célula">
                <BadgeAberto className="bg-[var(--ti-blueSoft,#eaf1fc)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:117" data-name="Célula">
                <BadgeBaixa className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:120" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:121">
                  Ontem, 16:40
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="3:122" data-name="Linha · #1030">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="3:123" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="3:124">
                  #1030
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="3:125" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="3:126">
                  Problema ao conectar ao Wi-Fi
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="3:127" data-name="Célula">
                <BadgeResolvido className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[85px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="3:130" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="3:133" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="3:134">
                  19 out, 11:05
                </p>
              </div>
            </div>
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:135">
            Você visualiza somente os chamados que abriu. · Dados de demonstração
          </p>
        </div>
      </div>
    </div>
  );
}
```

