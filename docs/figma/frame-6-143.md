# Referência Figma — frame 6:143

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=6-143

Contexto consultado em 21/10/2026 para revisão. Exemplos do design não são dados reais. Imagem retornada pelo conector; comparação com a aplicação renderizada permanece pendente.

```tsx
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

function BadgeEmAtendimento({ className }: { className?: string }) {
  return (
    <div className={className || "bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] w-[140px]"} data-node-id="2:45" data-name="Badge/Em atendimento">
      <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-amber,#9b600c)] whitespace-nowrap" data-node-id="2:46">
        Em atendimento
      </p>
    </div>
  );
}

export default function Component14MobileMeusChamados() {
  return (
    <div className="bg-[var(--ti-bg,#f4f7f6)] content-stretch flex flex-col items-start relative size-full" data-node-id="6:143" data-name="14 · Mobile · Meus chamados">
      <div className="[word-break:break-word] bg-[var(--ti-nav,#142d29)] content-stretch flex gap-[var(--ti-space-24,24px)] h-[72px] items-center leading-[1.45] not-italic overflow-clip p-[var(--ti-space-20,20px)] relative shrink-0 text-[color:var(--ti-white,white)] w-[390px] whitespace-nowrap" data-node-id="6:144" data-name="Cabeçalho mobile">
        <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px]" data-node-id="6:145">
          Nexo
        </p>
        <p className="font-['Inter:Medium'] font-medium relative shrink-0 text-[14px]" data-node-id="6:146">
          Menu
        </p>
      </div>
      <div className="content-stretch flex flex-col gap-[12px] items-start overflow-clip p-[var(--ti-space-20,20px)] relative shrink-0 w-[390px]" data-node-id="6:147" data-name="Conteúdo mobile">
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[41px] leading-[1.45] not-italic relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] w-[350px]" data-node-id="6:148">
          Olá, Marina.
        </p>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[21px] leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] w-[350px]" data-node-id="6:149">
          Como podemos ajudar hoje?
        </p>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[350px]" data-node-id="6:150" data-name="Button/Primary">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I6:150;2:38">
            + Abrir chamado
          </p>
        </div>
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[350px]" data-node-id="6:152" data-name="Input/Default">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I6:152;2:56">
            Buscar chamado…
          </p>
        </div>
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[16px] relative rounded-[12px] shrink-0 w-[350px]" data-node-id="6:154" data-name="Impressora do financeiro offline">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="6:155">
            #1048
          </p>
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[53px] leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] w-[302px]" data-node-id="6:156">
            Impressora do financeiro offline
          </p>
          <BadgeEmAtendimento className="bg-[var(--ti-amberSoft,#fff2da)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[120px]" />
        </div>
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[16px] relative rounded-[12px] shrink-0 w-[350px]" data-node-id="6:159" data-name="Acesso à pasta compartilhada">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="6:160">
            #1046
          </p>
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[27px] leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] w-[302px]" data-node-id="6:161">
            Acesso à pasta compartilhada
          </p>
          <BadgeAberto className="bg-[var(--ti-blueSoft,#eaf1fc)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[68px]" />
        </div>
        <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start overflow-clip p-[16px] relative rounded-[12px] shrink-0 w-[350px]" data-node-id="6:164" data-name="Problema ao conectar ao Wi-Fi">
          <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="6:165">
            #1030
          </p>
          <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[27px] leading-[1.45] not-italic relative shrink-0 text-[18px] text-[color:var(--ti-ink,#182c2a)] w-[302px]" data-node-id="6:166">
            Problema ao conectar ao Wi-Fi
          </p>
          <BadgeResolvido className="bg-[var(--ti-brandSoft,#e5f3ec)] content-stretch flex h-[28px] items-center justify-center relative rounded-[8px] shrink-0 w-[85px]" />
        </div>
      </div>
    </div>
  );
}
```

