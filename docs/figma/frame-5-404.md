# Referência Figma — frame 5:404

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=5-404

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

export default function Component12AdministradorDashboard() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="5:404" data-name="12 · Administrador · Dashboard">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="5:405" data-name="Navegação · Administrador">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:406" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="5:407">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:408">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="5:409">
          ÁREA DO ADMINISTRADOR
        </p>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:410" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:410;2:58">
            Dashboard
          </p>
        </div>
        <NavigationItem className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" />
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:414" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:414;2:58">
            Tarefas
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:416" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:416;2:58">
            Usuários
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:418" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:418;2:58">
            Logs
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="5:420" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:421" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="5:422">
            Douglas Lobo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:423">
            Administrador · T.I.
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:424">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="5:425" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="5:426" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="5:427">{`Workspace  /  Dashboard`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="5:428" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:429">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="5:430">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="5:431" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:432" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:433" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:434">
                Uma visão clara da operação.
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px]" data-node-id="5:435">
                Acompanhe o panorama global dos chamados da empresa.
              </p>
            </div>
          </div>
          <div className="[word-break:break-word] content-stretch flex gap-[var(--ti-space-16,16px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1128px] whitespace-nowrap" data-node-id="5:436" data-name="Indicadores">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[270px]" data-node-id="5:437" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:437;2:60">
                Abertos
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I5:437;2:61">
                24
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:437;2:62">
                Aguardando atendimento
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[270px]" data-node-id="5:441" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:441;2:60">
                Em andamento
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I5:441;2:61">
                18
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:441;2:62">
                Análise e atendimento
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[270px]" data-node-id="5:445" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:445;2:60">
                Finalizados
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I5:445;2:61">
                86
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:445;2:62">
                Resolvidos ou fechados
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[270px]" data-node-id="5:449" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:449;2:60">
                Não classificados
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I5:449;2:61">
                02
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:449;2:62">
                Revise a classificação
              </p>
            </div>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="5:453" data-name="Distribuição e totais">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[720px]" data-node-id="5:454" data-name="Distribuição dos chamados">
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:455">
                Onde estão os 130 chamados
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:456">
                Distribuição por grupo de status
              </p>
              <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[40px] items-center overflow-clip relative shrink-0 w-[672px]" data-node-id="5:457" data-name="Abertos">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[160px]" data-node-id="5:458">
                  Abertos
                </p>
                <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex h-[10px] items-start overflow-clip relative rounded-[6px] shrink-0 w-[400px]" data-node-id="5:459" data-name="Barra">
                  <div className="bg-[var(--ti-blue,#275eaa)] h-[10px] relative rounded-[6px] shrink-0 w-[73.846px]" data-node-id="5:460" data-name="Valor" />
                </div>
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:461">
                  24
                </p>
              </div>
              <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[40px] items-center overflow-clip relative shrink-0 w-[672px]" data-node-id="5:462" data-name="Em andamento">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[160px]" data-node-id="5:463">
                  Em andamento
                </p>
                <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex h-[10px] items-start overflow-clip relative rounded-[6px] shrink-0 w-[400px]" data-node-id="5:464" data-name="Barra">
                  <div className="bg-[var(--ti-amber,#9b600c)] h-[10px] relative rounded-[6px] shrink-0 w-[55.385px]" data-node-id="5:465" data-name="Valor" />
                </div>
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:466">
                  18
                </p>
              </div>
              <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[40px] items-center overflow-clip relative shrink-0 w-[672px]" data-node-id="5:467" data-name="Finalizados">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[160px]" data-node-id="5:468">
                  Finalizados
                </p>
                <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex h-[10px] items-start overflow-clip relative rounded-[6px] shrink-0 w-[400px]" data-node-id="5:469" data-name="Barra">
                  <div className="bg-[var(--ti-brand,#16765b)] h-[10px] relative rounded-[6px] shrink-0 w-[264.615px]" data-node-id="5:470" data-name="Valor" />
                </div>
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:471">
                  86
                </p>
              </div>
              <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[40px] items-center overflow-clip relative shrink-0 w-[672px]" data-node-id="5:472" data-name="Não classificados">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[160px]" data-node-id="5:473">
                  Não classificados
                </p>
                <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex h-[10px] items-start overflow-clip relative rounded-[6px] shrink-0 w-[400px]" data-node-id="5:474" data-name="Barra">
                  <div className="bg-[var(--ti-muted,#647773)] h-[10px] relative rounded-[6px] shrink-0 w-[6.154px]" data-node-id="5:475" data-name="Valor" />
                </div>
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:476">
                  2
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[384px]" data-node-id="5:477" data-name="Total global">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:478">
                TOTAL DE CHAMADOS
              </p>
              <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:479">
                130
              </p>
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[336px]" data-node-id="5:480">
                Cada chamado é contado uma vez, mesmo com vários técnicos associados.
              </p>
              <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[336px]" data-node-id="5:481" data-name="Button/Secondary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I5:481;2:40">
                  Consultar chamados
                </p>
              </div>
            </div>
          </div>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[1128px]" data-node-id="5:483" data-name="Atalhos administrativos">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:484">
              Acesso rápido
            </p>
            <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[48px] items-start overflow-clip relative shrink-0 w-[1080px]" data-node-id="5:485" data-name="Atalhos">
              <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[210px]" data-node-id="5:486" data-name="Button/Secondary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I5:486;2:40">
                  Cadastrar usuário
                </p>
              </div>
              <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[210px]" data-node-id="5:488" data-name="Button/Secondary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I5:488;2:40">
                  Consultar tarefas
                </p>
              </div>
              <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[210px]" data-node-id="5:490" data-name="Button/Secondary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I5:490;2:40">
                  Histórico e CSV
                </p>
              </div>
            </div>
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:492">
            Dados de demonstração · Proposta de interface
          </p>
        </div>
      </div>
    </div>
  );
}
```

