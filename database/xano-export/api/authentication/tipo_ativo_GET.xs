// Return safe tipo_ativo lookup fields to authenticated callers.
query tipo_ativo verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $verified_actor
    db.query tipo_ativo {
      return = {type: "list"}
    } as $tipo_ativo_rows

    array.map ($tipo_ativo_rows) {
      by = {
        id       : $this.id
        nome     : $this.nome
        descricao: $this.descricao
      }
    } as $tipo_ativo
  }

  response = $tipo_ativo
  guid = "JwOji1LhwiE7zpHtQ5cAj1agARg"
}
