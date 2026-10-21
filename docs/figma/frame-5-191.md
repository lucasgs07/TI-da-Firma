# Referência Figma — frame 5:191

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=5-191

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

export default function Component09GestorChamadosDoDepartamento() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="5:191" data-name="09 · Gestor · Chamados do departamento">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="5:192" data-name="Navegação · Gestor">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:193" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="5:194">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:195">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="5:196">
          ÁREA DO GESTOR
        </p>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:197" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:197;2:58">
            Chamados
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:199" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:199;2:58">
            Abrir chamado
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:201" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:201;2:58">
            Cadastrar usuário
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:203" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:203;2:58">
            Nova tarefa
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="5:205" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:206" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="5:207">
            Camila Santos
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:208">
            Gestor · Financeiro
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:209">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="5:210" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="5:211" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="5:212">{`Workspace  /  Chamados`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="5:213" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:214">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="5:215">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="5:216" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1124px]" data-node-id="5:217" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[900px]" data-node-id="5:218" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:219">
                Visibilidade para cuidar da equipe.
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[850px]" data-node-id="5:220">
                Financeiro · Chamados dos membros do seu departamento.
              </p>
            </div>
            <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:221" data-name="Button/Primary">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:221;2:38">
                + Abrir chamado
              </p>
            </div>
          </div>
          <div className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex gap-[var(--ti-space-12,12px)] items-start overflow-clip p-[var(--ti-space-16,16px)] relative rounded-[8px] shrink-0 w-[1128px]" data-node-id="5:223" data-name="Orientação">
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] w-[1096px]" data-node-id="5:224">
              Seu escopo é o departamento Financeiro. Os chamados são exibidos para consulta.
            </p>
          </div>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[12px] shrink-0 w-[1128px]" data-node-id="5:225" data-name="Tabela">
            <div className="[word-break:break-word] bg-[var(--ti-bg,#f4f7f6)] content-stretch flex font-['Inter:Regular'] font-normal h-[48px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] w-[1128px]" data-node-id="5:226" data-name="Cabeçalho da tabela">
              <p className="h-[18px] relative shrink-0 w-[80px]" data-node-id="5:227">
                Nº
              </p>
              <p className="h-[18px] relative shrink-0 w-[380px]" data-node-id="5:228">
                Solicitação
              </p>
              <p className="h-[18px] relative shrink-0 w-[200px]" data-node-id="5:229">
                Status
              </p>
              <p className="h-[18px] relative shrink-0 w-[150px]" data-node-id="5:230">
                Prioridade
              </p>
              <p className="h-[18px] relative shrink-0 w-[286px]" data-node-id="5:231">
                Solicitante
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:232" data-name="Linha · #1048">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="5:233" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="5:234">
                  #1048
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="5:235" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="5:236">
                  Impressora do financeiro offline
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="5:237" data-name="Célula">
                <BadgeEmAtendimento className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[120px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="5:240" data-name="Célula">
                <BadgeAlta className="bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="5:243" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="5:244">
                  Marina Costa
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:245" data-name="Linha · #1046">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="5:246" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="5:247">
                  #1046
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="5:248" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="5:249">
                  Acesso à pasta compartilhada
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="5:250" data-name="Célula">
                <BadgeAberto className="bg-[var(--ti-blueSoft,#eaf1fc)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="5:253" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="5:256" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="5:257">
                  Carlos Oliveira
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:258" data-name="Linha · #1030">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="5:259" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="5:260">
                  #1030
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="5:261" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="5:262">
                  Problema ao conectar ao Wi-Fi
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[200px]" data-node-id="5:263" data-name="Célula">
                <BadgeResolvido className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[85px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="5:266" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[286px]" data-node-id="5:269" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[270px]" data-node-id="5:270">
                  Marina Costa
                </p>
              </div>
            </div>
          </div>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[12px] shrink-0 w-[1128px]" data-node-id="5:271" data-name="Organização da equipe">
            <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:272">
              Próximos passos
            </p>
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1080px]" data-node-id="5:273">
              Crie tarefas para os funcionários do Financeiro ou cadastre um novo integrante do departamento.
            </p>
            <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[48px] items-start overflow-clip relative shrink-0 w-[1080px]" data-node-id="5:274" data-name="Atalhos">
              <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[160px]" data-node-id="5:275" data-name="Button/Primary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:275;2:38">
                  Nova tarefa
                </p>
              </div>
              <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:277" data-name="Button/Secondary">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I5:277;2:40">
                  Cadastrar usuário
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

