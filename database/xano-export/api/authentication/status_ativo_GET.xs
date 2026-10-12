// Return safe status_ativo lookup fields to authenticated callers.
query status_ativo verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query status_ativo {
      return = {type: "list"}
    } as $status_ativo_rows
  
    array.map ($status_ativo_rows) {
      by = {
        id       : $this.id
        nome     : $this.nome
        descricao: $this.descricao
      }
    } as $status_ativo
  }

  response = $status_ativo
  guid = "ZpUQuGKGT8E1NbmV-mi8tPRxfBk"
}