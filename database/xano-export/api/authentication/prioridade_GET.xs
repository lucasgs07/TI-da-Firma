// Return safe prioridade lookup fields to authenticated callers.
query prioridade verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $verified_actor
    db.query prioridade {
      return = {type: "list"}
    } as $prioridade_rows

    array.map ($prioridade_rows) {
      by = {id: $this.id, nome: $this.nome, nivel: $this.nivel}
    } as $prioridade
  }

  response = $prioridade
  guid = "rinWeduIa40uiuHjx6ddJJPdc2I"
}
