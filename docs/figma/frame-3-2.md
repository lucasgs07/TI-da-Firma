# Referência Figma — frame 3:2

Origem: https://www.figma.com/design/iogesOf6wVBdGExEIWrx2j?node-id=3-2

Contexto consultado em 21/10/2026 para revisão. Exemplos do design não são dados reais. Imagem retornada pelo conector; comparação com a aplicação renderizada permanece pendente.

```tsx
export default function Component01Login() {
  return (
    <div className="bg-[var(--ti-surface,white)] content-stretch flex items-start relative size-full" data-node-id="3:2" data-name="01 · Login">
      <div className="bg-[var(--ti-nav,#142d29)] content-stretch flex flex-col gap-[var(--ti-space-32,32px)] h-[1000px] items-start overflow-clip p-[64px] relative shrink-0 w-[660px]" data-node-id="3:3" data-name="Apresentação">
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[28px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="3:4">
          Nexo
        </p>
        <div className="h-[100px] relative shrink-0 w-[500px]" data-node-id="3:5" data-name="Respiro" />
        <div className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold h-[93px] leading-[0] not-italic relative shrink-0 text-[32px] text-[color:var(--ti-white,white)] w-[500px]" data-node-id="3:6">
          <p className="leading-[1.45] mb-0">Menos ruído.</p>
          <p className="leading-[1.45]">Mais solução.</p>
        </div>
        <div className="[word-break:break-word] font-['Inter:Regular'] font-normal h-[41px] leading-[0] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-navText,#b8ccc6)] w-[500px]" data-node-id="3:7">
          <p className="leading-[1.45] mb-0">Pessoas, chamados e tarefas no mesmo lugar.</p>
          <p className="leading-[1.45]">Seu trabalho flui melhor quando tudo se conecta.</p>
        </div>
        <div className="[word-break:break-word] bg-[var(--ti-brand,#16765b)] content-stretch flex flex-col gap-[var(--ti-space-20,20px)] items-start leading-[1.45] not-italic overflow-clip p-[var(--ti-space-24,24px)] relative rounded-[16px] shrink-0 text-[color:var(--ti-white,white)] w-[500px]" data-node-id="3:8" data-name="Prévia de atendimento">
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] whitespace-nowrap" data-node-id="3:9">
            DO PEDIDO À SOLUÇÃO
          </p>
          <p className="font-['Inter:Semi_Bold'] font-semibold relative shrink-0 text-[18px] whitespace-nowrap" data-node-id="3:10">
            Impressora do financeiro offline
          </p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[14px] whitespace-pre" data-node-id="3:11">{`#1048  ·  Em atendimento`}</p>
          <p className="font-['Inter:Regular'] font-normal relative shrink-0 text-[12px] whitespace-nowrap" data-node-id="3:12">
            Lucas e Pedro estão cuidando disso.
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-navText,#b8ccc6)] whitespace-nowrap" data-node-id="3:13">
          Uma central para toda a firma.
        </p>
      </div>
      <div className="content-stretch flex flex-col gap-[var(--ti-space-24,24px)] h-[1000px] items-start justify-center overflow-clip p-[100px] relative shrink-0 w-[780px]" data-node-id="3:14" data-name="Autenticação">
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-brand,#16765b)] whitespace-nowrap" data-node-id="3:15">
          BEM-VINDO DE VOLTA
        </p>
        <p className="[word-break:break-word] font-['Inter:Semi_Bold'] font-semibold leading-[1.45] not-italic relative shrink-0 text-[28px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:16">
          Entre no seu workspace
        </p>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:17">
          Use suas credenciais corporativas.
        </p>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[580px]" data-node-id="3:18" data-name="E-mail">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:19">
            E-mail
          </p>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[580px]" data-node-id="3:20" data-name="Input/Default">
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I3:20;2:56">
              voce@empresa.com.br
            </p>
          </div>
        </div>
        <div className="content-stretch flex flex-col gap-[var(--ti-space-8,8px)] items-start overflow-clip relative shrink-0 w-[580px]" data-node-id="3:22" data-name="Senha">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-ink,#182c2a)] whitespace-nowrap" data-node-id="3:23">
            Senha
          </p>
          <div className="bg-[var(--ti-surface,white)] border border-[var(--ti-border,#dfe7e4)] border-solid content-stretch flex h-[48px] items-center pl-[14px] relative rounded-[8px] shrink-0 w-[580px]" data-node-id="3:24" data-name="Input/Default">
            <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="I3:24;2:56">
              ••••••••
            </p>
          </div>
        </div>
        <div className="bg-[var(--ti-brand,#16765b)] content-stretch flex h-[44px] items-center justify-center relative rounded-[8px] shrink-0 w-[580px]" data-node-id="3:26" data-name="Button/Primary">
          <p className="[word-break:break-word] font-['Inter:Medium'] font-medium leading-[1.45] not-italic relative shrink-0 text-[14px] text-[color:var(--ti-white,white)] whitespace-nowrap" data-node-id="I3:26;2:38">
            Entrar
          </p>
        </div>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:28">
          Precisa de acesso? Fale com o administrador.
        </p>
        <p className="[word-break:break-word] font-['Inter:Regular'] font-normal leading-[1.45] not-italic relative shrink-0 text-[12px] text-[color:var(--ti-muted,#647773)] whitespace-nowrap" data-node-id="3:29">
          Sua área é definida automaticamente pelo seu perfil.
        </p>
      </div>
    </div>
  );
}
```

