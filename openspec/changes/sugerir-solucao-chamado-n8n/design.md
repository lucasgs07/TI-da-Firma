# Design

## Context

O painel em `TI_da_Firma/technician_portal.py` já condiciona a edição de **Solução final** a `AuthState.pode_atualizar_atendimento`. O PATCH de chamado verifica perfil técnico, associação via `chamado_tecnico` com compatibilidade para responsável legado e bloqueio de atendimento encerrado. A proposta adiciona uma consulta ao lado desse fluxo.

## Goals / Non-Goals

- Reaproveitar a elegibilidade do painel e as regras de associação e sessão do backend.
- Usar o fluxo n8n existente para produzir sugestões isoladas do formulário de edição. O processo atual de salvar e resolver continua sob controle do técnico.

## Decisions

1. **Consulta via Xano.** O Reflex envia o ID do chamado pelo cliente autenticado. O Xano verifica a sessão, a associação e o estado do chamado antes de acionar o webhook. URL e credenciais ficam em configuração do backend. O payload usa somente os dados do chamado necessários ao fluxo, definidos ao conferir seu contrato.
2. **Resposta estruturada.** O Xano valida e normaliza as sugestões, incluindo título ou descrição, passos e referência opcional. Uma referência só é exibida se a autorização puder ser verificada. O Reflex renderiza os campos como texto.
3. **Modal ligado à consulta.** O clique abre o modal com estado de carregamento. O resultado pertence ao chamado e à sessão que iniciaram a busca. O botão **Fechar** devolve o foco à ação quando disponível, e o formulário mantém seu conteúdo.

## Risks / Trade-offs

- [Fluxo lento ou indisponível] → limitar o tempo da chamada e oferecer nova tentativa manual.
- [Dados internos em respostas ou referências] → minimizar o contexto enviado, validar a resposta e omitir referências sem autorização.

## Migration Plan

Validar o contrato com o fluxo de teste, publicar a operação Xano de acordo com o processo do projeto e então habilitar a ação no Reflex. Em caso de reversão, retirar a ação e desativar a integração. A entrega usa os registros e campos existentes.

## Open Questions

- O endereço do webhook foi fornecido durante o apply. Um POST com dados fictícios retornou HTTP 403 com a mensagem `Authorization data is wrong!`. Confirmar o esquema de autenticação e obter exemplos sanitizados de entrada e saída antes de concluir a integração.
- O cliente Reflex espera um contrato interno normalizado no formato `{"sugestoes":[{"titulo":"…","passos":["…"],"referencia":"…"}]}`. A lista vazia indica ausência de sugestões. Esse formato pertence à API do Xano e ainda precisa ser mapeado a partir da resposta real do n8n.
- O adaptador local aponta para o webhook de produção. Configure no Xano `N8N_SUGGESTION_HEADER_NAME` e `N8N_SUGGESTION_HEADER_VALUE` com a credencial Header Auth correspondente. A primeira versão do adaptador espera `sugestoes` na resposta do n8n e projeta título e passos. A exibição de referências depende de confirmar o formato do identificador e aplicar a autorização correspondente no Xano.
