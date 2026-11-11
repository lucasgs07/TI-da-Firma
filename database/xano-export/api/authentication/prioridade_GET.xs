// Return safe prioridade lookup fields to authenticated callers.
query prioridade verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query prioridade {
      return = {type: "list"}
    } as $prioridade_rows
  
    array.map ($prioridade_rows) {
      by = {
        id       : $this.id
        nome     : $this.nome
        nivel    : $this.nivel
        sla_horas: $this.sla_horas
      }
    } as $prioridade
  }

  response = $prioridade
  guid = "rinWeduIa40uiuHjx6ddJJPdc2I"
}