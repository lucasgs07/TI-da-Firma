// Get a safe status_chamado lookup record.
query "status_chamado/{status_chamado_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int status_chamado_id filters=min:1
  }

  stack {
    db.get status_chamado {
      field_name = "id"
      field_value = $input.status_chamado_id
    } as $status_chamado
  
    precondition ($status_chamado != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    var $safe_status_chamado {
      value = {id: $status_chamado.id, nome: $status_chamado.nome}
    }
  }

  response = $safe_status_chamado
  guid = "VWtWbSzcxhySl1BMVXZfzkMyAhY"
}