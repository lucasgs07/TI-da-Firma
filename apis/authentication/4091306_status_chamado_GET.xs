// Return safe status_chamado lookup fields to authenticated callers.
query status_chamado verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $verified_actor
    db.query status_chamado {
      return = {type: "list"}
    } as $status_chamado_rows

    array.map ($status_chamado_rows) {
      by = {id: $this.id, nome: $this.nome}
    } as $status_chamado
  }

  response = $status_chamado
  guid = "334eSKUyWDBTnvXQ-Gqxir9szNk"
}
