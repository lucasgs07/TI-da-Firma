// Get a safe status_ativo lookup record.
query "status_ativo/{status_ativo_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int status_ativo_id filters=min:1
  }

  stack {
    db.get status_ativo {
      field_name = "id"
      field_value = $input.status_ativo_id
    } as $status_ativo
  
    precondition ($status_ativo != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    var $safe_status_ativo {
      value = {
        id       : $status_ativo.id
        nome     : $status_ativo.nome
        descricao: $status_ativo.descricao
      }
    }
  }

  response = $safe_status_ativo
  guid = "sOOfA8ozJOi35TbBmrQpeoxfCYU"
}