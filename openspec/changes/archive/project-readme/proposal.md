# Proposal

## Why

O repositório não tem um README na raiz que apresente o propósito, os perfis e o estado atual da Plataforma de Gestão Interna Empresarial a avaliadores. Uma visão geral concisa facilitará a compreensão do projeto e apontará para a documentação detalhada sem confundir funcionalidades planejadas com validações ainda pendentes.

## What Changes

- Criar `README.md` na raiz, em português brasileiro e direcionado principalmente a avaliadores.
- Apresentar o problema e objetivo do sistema, a arquitetura Reflex + Xano e um resumo dos perfis e fluxos já documentados.
- Distinguir funcionalidades implementadas, escopo planejado para o MVP e validações ainda pendentes, sem afirmar publicação ou conclusão não comprovadas.
- Incluir instrução breve de configuração/execução baseada nas instruções versionadas e links para a documentação existente.
- Não alterar código, APIs, banco de dados, configuração de execução ou a documentação existente.

## Capabilities

### New Capabilities

Nenhuma. Esta mudança entrega documentação do projeto e não introduz comportamento de sistema.

### Modified Capabilities

Nenhuma. As especificações existentes de autenticação e portais não têm seus requisitos alterados.

Esta mudança declara `skip_specs: true` em `.openspec.yaml`, pois não há alteração de comportamento a especificar.

## Impact

Somente `README.md` será criado na raiz do repositório. A redação usará como fontes os documentos existentes em `docs/`, as dependências e configuração Reflex versionadas, e as especificações e registros OpenSpec relevantes. Não adiciona dependências nem requer alteração no Xano.
