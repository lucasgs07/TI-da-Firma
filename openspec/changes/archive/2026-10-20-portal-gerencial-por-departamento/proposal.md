# Proposal

## Why

O frontend Reflex ainda apresenta uma home genérica para gestores, sem as operações gerenciais existentes no Xano. As permissões atuais também não distinguem adequadamente o gerente de T.I. dos demais gestores para criação de usuários e tarefas.

## What Changes

- Disponibilizar uma área gerencial para o perfil Gestor (`perfil_id` 2), com recursos determinados pelo departamento autenticado.
- Gerente de T.I.: consultar todos os chamados em modo de leitura, abrir chamados e criar tarefas atribuídas somente a técnicos de T.I.
- Gerente de T.I.: cadastrar funcionários e gestores em qualquer departamento e técnicos obrigatoriamente em T.I.; não poderá cadastrar administradores.
- Demais gestores: consultar chamados abertos por membros do próprio departamento, abrir seus próprios chamados, cadastrar somente funcionários no próprio departamento e criar tarefas atribuídas a esses funcionários.
- Funcionários: consultar somente as tarefas atribuídas a eles e concluí-las com solução obrigatória, sem ganhar permissão para atender ou resolver chamados.
- Técnicos e funcionários: acessar Minhas tarefas em tela própria, separada de Chamados; técnicos também consultam e concluem suas tarefas atribuídas, preservando suas autorizações existentes.
- Tarefas podem ter vários responsáveis elegíveis. Qualquer associado pode concluir a tarefa inteira com solução obrigatória; todos consultam o mesmo status e solução.
- Garantir o vínculo obrigatório de novos técnicos à T.I. também no cadastro por administrador, sem migrar ou excluir usuários existentes automaticamente.
- Corrigir as autorizações no Xano, incluindo consultas individuais e requisições diretas, além dos controles das telas.

## Capabilities

### New Capabilities

- `manager-portal`: telas gerenciais, cadastro e atribuição departamental de tarefas e consulta/conclusão de tarefas próprias pelo funcionário.

### Modified Capabilities

Nenhuma das capacidades principais existentes precisa mudar seus requisitos. Os portais de funcionário e técnico permanecem separados, e autenticação continua usando a sessão existente.

## Impact

- Frontend Reflex: home, estado de sessão, novos componentes gerenciais e cliente HTTP; reutilizar partes visuais/formulários sem liberar eventos exclusivos do funcionário ou técnico.
- Backend Xano: `get_actor_scope`, regras de cadastro e seleção de usuários, autorização de responsável de tarefa, criação de tarefas e escopo de leitura de chamados/interações. Consultar os consumidores dos helpers para evitar ampliação indireta de operações.
- Dados: reutilizar as entidades existentes e acrescentar à tabela `tarefa` o campo opcional de referência múltipla `responsaveis_ids`. Preservar `responsavel_id` como compatibilidade, sem excluir dados ou exigir migração em massa de tarefas antigas. Não há nova tabela prevista.
- **BREAKING:** gestores de outros departamentos perdem a permissão atual de criar técnicos; suas tarefas passam a ser atribuídas exclusivamente a funcionários do próprio departamento. Novos técnicos não poderão ser criados fora de T.I. A leitura departamental passa de solicitantes funcionários para membros do departamento de qualquer perfil.
- A mudança ampla `estrutura-inicial-do-modulo-de-chamados` continua sendo planejamento; `portal-atendimento-tecnico` tem implementação e validações próprias ainda em acompanhamento. Nenhuma delas será arquivada ou marcada como concluída por esta proposta.
- Premissas de escopo: “função” significa perfil; chamados gerenciais são de consulta, sem atribuição, comentários ou alteração de status nesta área. Inclui conclusão de tarefas pelo funcionário responsável; preserva a conclusão já autorizada ao técnico. Não inclui edição de usuários existentes, administração de perfis/departamentos, nova tela de reatribuição de tarefas ou indicadores.
- A configuração existente identifica T.I. por `departamento_id` 1; verificar sua consistência antes de publicar, sem criar outro identificador por suposição. Publicação remota exige simulação e autorização específica, ainda não concedida para esta mudança.
