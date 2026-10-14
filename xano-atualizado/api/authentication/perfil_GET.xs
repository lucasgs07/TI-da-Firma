// Return safe perfil lookup fields to authenticated callers.
query perfil verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    db.query perfil {
      return = {type: "list"}
    } as $perfil_rows
  
    array.map ($perfil_rows) {
      by = {
        id       : $this.id
        name     : $this.name
        descricao: $this.descricao
      }
    } as $perfil
  }

  response = $perfil
  guid = "uEx8oeeWz9fFDM3mgBk7eyQ_Pr8"
}