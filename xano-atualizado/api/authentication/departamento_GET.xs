// Return safe departamento lookup fields to authenticated callers.
query departamento verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query departamento {
      return = {type: "list"}
    } as $departamento_rows
  
    array.map ($departamento_rows) {
      by = {id: $this.id, nome: $this.nome}
    } as $departamento
  }

  response = $departamento
  guid = "2KkAmIABREU9rTbmB3P9l9TSVqY"
}