// Return safe categoria_chamado lookup fields to authenticated callers.
query categoria_chamado verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $verified_actor
    db.query categoria_chamado {
      return = {type: "list"}
    } as $categoria_chamado_rows

    array.map ($categoria_chamado_rows) {
      by = {id: $this.id, nome: $this.nome}
    } as $categoria_chamado
  }

  response = $categoria_chamado
  guid = "UjVry0rqAcd4nj97AOEEQh5Gabg"
}
