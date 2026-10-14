// Get a safe categoria_chamado lookup record.
query "categoria_chamado/{categoria_chamado_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int categoria_chamado_id filters=min:1
  }

  stack {
    db.get categoria_chamado {
      field_name = "id"
      field_value = $input.categoria_chamado_id
    } as $categoria_chamado
  
    precondition ($categoria_chamado != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    var $safe_categoria_chamado {
      value = {id: $categoria_chamado.id, nome: $categoria_chamado.nome}
    }
  }

  response = $safe_categoria_chamado
  guid = "q70LP9AGBSuoXqPdT68qAqN01qY"
}