# Referência Figma — frame 5:64

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=5-64

Contexto consultado em 21/10/2026 para revisão. Exemplos do design não são dados reais. Imagem retornada pelo conector; comparação com a aplicação renderizada permanece pendente.

```tsx
function BadgeBaixa({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:53" data-name="Badge/Baixa">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="2:54">
        Baixa
      </p>
    </div>
  );
}

function BadgeMedia({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:51" data-name="Badge/Média">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-amber,#9b600c)] whitespace-nowrap" data-node-id="2:52">
        Média
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

export default function Component07FuncionarioMinhasTarefas() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="5:64" data-name="07 · Funcionário · Minhas tarefas">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="5:65" data-name="Navegação · Funcionário">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:66" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="5:67">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:68">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="5:69">
          ÁREA DO FUNCIONÁRIO
        </p>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:70" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:70;2:58">
            Meus chamados
          </p>
        </div>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:72" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:72;2:58">
            Minhas tarefas
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="5:74" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:75" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="5:76">
            Marina Costa
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:77">
            Funcionário · Financeiro
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:78">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="5:79" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="5:80" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="5:81">{`Workspace  /  Minhas tarefas`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="5:82" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:83">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="5:84">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="5:85" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:86" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:87" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:88">
                Seu trabalho, organizado.
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px]" data-node-id="5:89">
                Veja as tarefas atribuídas a você e registre a solução ao concluir.
              </p>
            </div>
          </div>
          <div className="[word-break:break-word] content-stretch flex gap-[var(--ti-space-16,16px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[516px] whitespace-nowrap" data-node-id="5:90" data-name="Resumo das tarefas">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[250px]" data-node-id="5:91" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:91;2:60">
                Pendentes
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I5:91;2:61">
                03
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:91;2:62">
                Tarefas atribuídas a você
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[8px] h-[140px] items-start pl-[20px] pt-[20px] relative rounded-[12px] shrink-0 w-[250px]" data-node-id="5:95" data-name="Metric/Card">
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:95;2:60">
                Concluídas
              </p>
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[32px] text-[color:var(--ti-ink,#182c2a)]" data-node-id="I5:95;2:61">
                12
              </p>
              <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)]" data-node-id="I5:95;2:62">
                Tarefas atribuídas a você
              </p>
            </div>
          </div>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[12px] shrink-0 w-[1128px]" data-node-id="5:99" data-name="Tabela">
            <div className="[word-break:break-word] bg-[var(--ti-bg,#f4f7f6)] content-stretch flex font-['Inter:Regular'] font-normal h-[48px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] w-[1128px]" data-node-id="5:100" data-name="Cabeçalho da tabela">
              <p className="h-[18px] relative shrink-0 w-[80px]" data-node-id="5:101">
                Tarefa
              </p>
              <p className="h-[18px] relative shrink-0 w-[380px]" data-node-id="5:102">
                Atividade
              </p>
              <p className="h-[18px] relative shrink-0 w-[150px]" data-node-id="5:103">
                Prioridade
              </p>
              <p className="h-[18px] relative shrink-0 w-[180px]" data-node-id="5:104">
                Prazo
              </p>
              <p className="h-[18px] relative shrink-0 w-[306px]" data-node-id="5:105">
                Responsáveis
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:106" data-name="Linha · #208">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="5:107" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="5:108">
                  #208
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="5:109" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="5:110">
                  Validar impressora do setor
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="5:111" data-name="Célula">
                <BadgeAlta className="bg-[var(--ti-redSoft,#fcecec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[180px]" data-node-id="5:114" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[164px]" data-node-id="5:115">
                  Hoje
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[306px]" data-node-id="5:116" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[290px]" data-node-id="5:117">
                  Marina, Carlos
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:118" data-name="Linha · #204">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="5:119" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="5:120">
                  #204
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="5:121" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="5:122">
                  Conferir acesso à pasta de custos
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="5:123" data-name="Célula">
                <BadgeMedia className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[180px]" data-node-id="5:126" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[164px]" data-node-id="5:127">
                  23 out
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[306px]" data-node-id="5:128" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[290px]" data-node-id="5:129">
                  Marina Costa
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:130" data-name="Linha · #199">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[80px]" data-node-id="5:131" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[64px]" data-node-id="5:132">
                  #199
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[380px]" data-node-id="5:133" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[364px]" data-node-id="5:134">
                  Revisar equipamentos da sala
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[150px]" data-node-id="5:135" data-name="Célula">
                <BadgeBaixa className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[180px]" data-node-id="5:138" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[164px]" data-node-id="5:139">
                  25 out
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[306px]" data-node-id="5:140" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[290px]" data-node-id="5:141">
                  Marina Costa
                </p>
              </div>
            </div>
          </div>
          <div className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex gap-[var(--ti-space-12,12px)] items-start overflow-clip p-[var(--ti-space-16,16px)] relative rounded-[8px] shrink-0 w-[1128px]" data-node-id="5:142" data-name="Orientação">
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] w-[1096px]" data-node-id="5:143">
              Qualquer responsável pode concluir a tarefa inteira. A solução fica registrada para todos.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
```

