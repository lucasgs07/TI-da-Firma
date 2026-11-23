# Tasks

## 1. Contrato e integração Xano

- [ ] 1.1 Confirmar webhook, autenticação e exemplos sanitizados do n8n. Validar o mapeamento de sugestões, referências e resposta vazia no fluxo de teste.
- [ ] 1.2 Implementar a consulta autenticada no Xano e testar os casos de técnico associado, responsável legado, técnico sem associação, chamado encerrado e outros perfis. Confirmar que casos negados não disparam o fluxo.
- [ ] 1.3 Integrar o webhook e validar a resposta. Testar retorno válido, lista vazia, resposta inválida, tempo limite e referências sem autorização. Registrar o contrato sem credenciais.

## 2. Atendimento no Reflex

- [ ] 2.1 Integrar o cliente e o estado de consulta. Testar clique duplicado, nova tentativa, troca de chamado e encerramento de sessão durante uma solicitação.
- [ ] 2.2 Adicionar o botão e o modal com base nas imagens. Verificar a visibilidade por perfil, os estados de busca e resultado, a navegação por teclado e a preservação do rascunho ao fechar.

## 3. Validação integrada

- [ ] 3.1 Verificar o fluxo completo em ambiente de teste com um técnico autorizado e com um usuário sem permissão. Confirmar a resposta no modal e comprovar que a consulta não grava a solução final nem altera o status.
