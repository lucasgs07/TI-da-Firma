# Design

## Context

Consulte [proposal.md](proposal.md) para a motivação e [specs/employee-ticket-portal/spec.md](specs/employee-ticket-portal/spec.md) para os comportamentos observáveis.

O frontend Reflex possui uma página autenticada genérica e um `AuthState` que conserva o perfil seguro retornado pelo Xano. O cliente HTTP atual cobre login e validação de sessão. No snapshot local do Xano já existem endpoints autenticados para listar, criar e consultar chamados, além de consultar categorias e prioridades. A listagem e a consulta individual usam o usuário autenticado para limitar chamados de perfil 4 ao próprio solicitante; a criação deriva o solicitante da sessão e resolve o status inicial pelo registro `Aberto`. O estado do snapshot local não comprova que os mesmos contratos estejam publicados no workspace remoto.

A tabela `categoria_chamado` exportada contém somente o schema; os nomes e identificadores esperados foram informados pelo usuário e precisam ser conferidos no Xano remoto durante a implementação.

## Goals / Non-Goals

**Goals:**
- Ligar as telas Reflex às consultas autenticadas existentes para listas, detalhe, abertura, categorias e prioridades.
- Usar o perfil seguro apenas para apresentar a experiência adequada; manter as decisões de autorização e a identidade do solicitante sob controle do backend.
- Tratar respostas de lista e objeto, estados vazios, carregamento, sessão rejeitada e falhas de serviço explicitamente.

**Non-Goals:**
- Criar ações de atendimento para funcionário, como atribuir chamados, alterar status ou registrar interações.
- Introduzir campos, categorias, prioridades, status ou tabelas que não existam nos contratos e nas estruturas verificadas.
- Alterar registros ou publicar mudanças no Xano remoto sem antes apresentar a simulação da alteração e obter autorização explícita.

## Decisions

### 1. Separar chamadas HTTP autenticadas da apresentação Reflex

Estender o cliente Xano existente com operações explícitas para os endpoints de chamados e tabelas de apoio; manter em `AuthState` a sessão e o perfil seguro, e manter os dados transitórios do fluxo em estado Reflex dedicado ou no estado existente, conforme o padrão que a implementação encontrar. Isso permite testar serialização, autorização e erros HTTP sem acoplar os testes à renderização.

**Alternativa considerada:** realizar requisições diretamente nos componentes da página. Foi descartada porque mistura transporte e apresentação, dificulta testar falhas e incentiva o uso de valores do formulário como fonte de autorização.

### 2. O backend define escopo e solicitante; o perfil só controla a experiência

O frontend deve enviar o token autenticado em cada chamada, não enviar `solicitante_id` como identidade confiável e não tentar substituir a filtragem do backend por filtros locais. O acesso direto ao detalhe deve chamar o endpoint individual; uma resposta sem autorização ou inexistente não pode deixar dados anteriores na tela.

**Alternativa considerada:** buscar todos os chamados e filtrar no navegador pelo usuário local. Foi descartada por expor dados alheios na resposta e depender de valores locais que não são uma fronteira de segurança.

### 3. Os lookups do Xano são a fonte das opções e identificadores

Carregar as opções pelas APIs autenticadas de lookup e submeter os IDs retornados por essas APIs. A lista inicialmente informada (`Hardware`, `Software`, `Rede`, `Acesso`, `Impressora` e `Outros`) não é uma lista fechada: categorias válidas retornadas pelo Xano devem permanecer selecionáveis mesmo quando os nomes, IDs ou quantidade divergirem. Não preencher opções ausentes nem fixar nomes ou IDs no formulário. As prioridades também devem ser obtidas do Xano.

**Alternativa considerada:** bloquear o formulário se a resposta do Xano não coincidir exatamente com os seis pares inicialmente informados. Foi descartada após a validação com o workspace real, pois impedia o uso de opções válidas existentes no Xano.

### 4. Manter o contrato existente de abertura se confirmado no ambiente remoto

O snapshot local define título, descrição, `categoria_chamado_id` e `prioridade_id` como entradas, e deixa solicitante e status inicial sob responsabilidade da API. Confirmar o contrato publicado antes da integração. Se houver divergência que exija alteração do workspace, preparar e apresentar `--dry-run` e aguardar autorização antes de executar push.

**Alternativa considerada:** adaptar ou publicar silenciosamente a API junto com as telas. Foi descartada para evitar alteração remota não autorizada e incompatibilidade com o estado real do banco.

## Risks / Trade-offs

- [Snapshot de APIs desatualizado] → Verificar os contratos e as categorias no Xano remoto durante a implementação; não declarar a integração pronta apenas com base nos arquivos exportados.
- [Resposta de um chamado fora do escopo] → Testar leitura de lista e consulta individual com solicitantes diferentes e limpar o detalhe anterior quando uma chamada falhar ou for negada.
- [Categorias ou status inicial ausentes] → Exibir erro de configuração e bloquear o envio; solicitar autorização e apresentar simulação antes de qualquer ajuste remoto.
- [Perfil local divergente da sessão] → Validar a sessão antes de abrir a área e depender da autorização no backend para cada registro.

## Migration Plan

1. Confirmar no Xano remoto a publicação dos endpoints e a correspondência dos registros de categoria informados, sem escrever no workspace.
2. Implementar cliente autenticado, estado e telas Reflex, preservando os fluxos de login e logout.
3. Executar testes direcionados para funcionário, escopo próprio, opções do formulário e falhas de API.
4. Se a verificação identificar uma alteração necessária no Xano, preparar dry-run, apresentar o impacto e aguardar autorização explícita antes de aplicar.
5. Para rollback do frontend, remover as telas e chamadas novas; a mudança não requer migração de dados se os registros informados já estiverem configurados.

## Open Questions

Nenhuma decisão funcional permanece pendente para esta proposta. A publicação dos contratos e a presença dos seis registros no workspace remoto são verificações de implementação, não requisitos para redefinir o escopo.
