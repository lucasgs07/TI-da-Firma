addon perfil {
  input {
    int perfil_id? {
      table = "perfil"
    }
  }

  stack {
    db.query perfil {
      where = $db.perfil.id == $input.perfil_id
      return = {type: "single"}
    }
  }

  guid = "d8H_qCN2fFG8q9qpkK7MZbnbGn0"
}