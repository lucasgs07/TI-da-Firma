# Referência Figma — frame 5:493

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=5-493

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

export default function Component13AdministradorHistoricoDeInteracoes() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex items-start relative size-full" data-node-id="5:493" data-name="13 · Administrador · Histórico de interações">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] h-[1000px] items-start overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[232px]" data-node-id="5:494" data-name="Navegação · Administrador">
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[84px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:495" data-name="Marca">
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] text-[color:var(--ti-white,white)]" data-node-id="5:496">
            Nexo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:497">
            GESTÃO INTERNA
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="5:498">
          ÁREA DO ADMINISTRADOR
        </p>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:499" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:499;2:58">
            Dashboard
          </p>
        </div>
        <NavigationItem className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" />
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:503" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:503;2:58">
            Tarefas
          </p>
        </div>
        <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:505" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="I5:505;2:58">
            Usuários
          </p>
        </div>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center pl-[16px] relative rounded-[8px] shrink-0 w-[200px]" data-node-id="5:507" data-name="Navigation/Item">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:507;2:58">
            Logs
          </p>
        </div>
        <div className="flex-[1_0_0] min-h-px relative w-[200px]" data-node-id="5:509" data-name="Espaço flexível" />
        <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] h-[92px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-12,12px)] relative shrink-0 w-[200px] whitespace-nowrap" data-node-id="5:510" data-name="Perfil">
          <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px] text-[color:var(--ti-white,white)]" data-node-id="5:511">
            Douglas Lobo
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:512">
            Administrador · T.I.
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)]" data-node-id="5:513">
            Sair da conta
          </p>
        </div>
      </div>
      <div className="content-stretch flex flex-col h-[1000px] items-start overflow-clip relative shrink-0 w-[1208px]" data-node-id="5:514" data-name="Conteúdo">
        <div className="bg-[var(--ti-surface,white)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center overflow-clip p-[var(--ti-space-24,24px)] relative shrink-0 w-[1208px]" data-node-id="5:515" data-name="Barra superior">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-pre" data-node-id="5:516">{`Workspace  /  Logs`}</p>
          <div className="flex-[1_0_0] h-[20px] min-w-px relative" data-node-id="5:517" data-name="Espaço" />
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:518">
            Ambiente interno
          </p>
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="5:519">
            DL
          </p>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] items-start overflow-clip p-[var(--ti-space-40,40px)] relative shrink-0 w-[1208px]" data-node-id="5:520" data-name="Área principal">
          <div className="content-stretch flex gap-[var(--ti-space-24,24px)] items-center overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:521" data-name="Cabeçalho">
            <div className="[word-break:break-word] content-stretch flex flex-col gap-[var(--ti-space-4,4px)] items-start leading-[1.45] not-italic overflow-clip relative shrink-0 w-[1100px]" data-node-id="5:522" data-name="Título">
              <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="5:523">
                O histórico, com contexto.
              </p>
              <p className="font-['Inter:Regular'] font-normal h-[21px] relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[1060px]" data-node-id="5:524">
                Consulte interações registradas e exporte o histórico completo.
              </p>
            </div>
          </div>
          <div className="content-stretch flex gap-[var(--ti-space-16,16px)] h-[48px] items-start overflow-clip relative shrink-0 w-[1128px]" data-node-id="5:525" data-name="Filtro e exportação">
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[500px]" data-node-id="5:526" data-name="Input/Default">
              <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I5:526;2:56">
                Nº do chamado · opcional
              </p>
            </div>
            <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[170px]" data-node-id="5:528" data-name="Button/Primary">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I5:528;2:38">
                Aplicar filtro
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[250px]" data-node-id="5:530" data-name="Button/Secondary">
              <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="I5:530;2:40">
                Baixar histórico CSV
              </p>
            </div>
          </div>
          <div className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex gap-[var(--ti-space-12,12px)] items-start overflow-clip p-[var(--ti-space-16,16px)] relative rounded-[8px] shrink-0 w-[1128px]" data-node-id="5:532" data-name="Orientação">
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-brand,#16765b)] w-[1096px]" data-node-id="5:533">
              Exibindo interações do chamado #1048. A exportação usa este filtro aplicado.
            </p>
          </div>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col items-start overflow-clip relative rounded-[12px] shrink-0 w-[1128px]" data-node-id="5:534" data-name="Tabela">
            <div className="[word-break:break-word] bg-[var(--ti-bg,#f4f7f6)] content-stretch flex font-['Inter:Regular'] font-normal h-[48px] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] w-[1128px]" data-node-id="5:535" data-name="Cabeçalho da tabela">
              <p className="h-[18px] relative shrink-0 w-[70px]" data-node-id="5:536">
                ID
              </p>
              <p className="h-[18px] relative shrink-0 w-[100px]" data-node-id="5:537">
                Chamado
              </p>
              <p className="h-[18px] relative shrink-0 w-[180px]" data-node-id="5:538">
                Autor
              </p>
              <p className="h-[18px] relative shrink-0 w-[210px]" data-node-id="5:539">
                Data (UTC−03:00)
              </p>
              <p className="h-[18px] relative shrink-0 w-[536px]" data-node-id="5:540">
                Mensagem
              </p>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:541" data-name="Linha · 301">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[70px]" data-node-id="5:542" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[54px]" data-node-id="5:543">
                  301
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[100px]" data-node-id="5:544" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[84px]" data-node-id="5:545">
                  #1048
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[180px]" data-node-id="5:546" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[164px]" data-node-id="5:547">
                  Marina Costa
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[210px]" data-node-id="5:548" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[194px]" data-node-id="5:549">
                  21 out, 09:10
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[536px]" data-node-id="5:550" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[520px]" data-node-id="5:551">
                  A impressora aparece offline.
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:552" data-name="Linha · 306">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[70px]" data-node-id="5:553" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[54px]" data-node-id="5:554">
                  306
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[100px]" data-node-id="5:555" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[84px]" data-node-id="5:556">
                  #1048
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[180px]" data-node-id="5:557" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[164px]" data-node-id="5:558">
                  Lucas Gomes
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[210px]" data-node-id="5:559" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[194px]" data-node-id="5:560">
                  21 out, 14:32
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[536px]" data-node-id="5:561" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[520px]" data-node-id="5:562">
                  Falha na configuração de rede.
                </p>
              </div>
            </div>
            <div className="bg-[var(--ti-surface,white)] content-stretch flex h-[72px] items-center overflow-clip p-[var(--ti-space-16,16px)] relative shrink-0 w-[1128px]" data-node-id="5:563" data-name="Linha · 310">
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[70px]" data-node-id="5:564" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[54px]" data-node-id="5:565">
                  310
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[100px]" data-node-id="5:566" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Medium'] font-medium h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[84px]" data-node-id="5:567">
                  #1048
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[180px]" data-node-id="5:568" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[164px]" data-node-id="5:569">
                  Pedro Lima
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[210px]" data-node-id="5:570" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[194px]" data-node-id="5:571">
                  21 out, 14:48
                </p>
              </div>
              <div className="content-stretch flex h-[36px] items-center overflow-clip relative shrink-0 w-[536px]" data-node-id="5:572" data-name="Célula">
                <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] w-[520px]" data-node-id="5:573">
                  Ajuste de conexão em validação.
                </p>
              </div>
            </div>
          </div>
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="5:574">
            Página 1 de 1 · 3 interações · Somente interações efetivamente registradas.
          </p>
        </div>
      </div>
    </div>
  );
}
```

