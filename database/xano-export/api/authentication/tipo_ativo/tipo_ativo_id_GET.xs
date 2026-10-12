// Get a safe tipo_ativo lookup record.
query "tipo_ativo/{tipo_ativo_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int tipo_ativo_id filters=min:1
  }

  stack {
    db.get tipo_ativo {
      field_name = "id"
      field_value = $input.tipo_ativo_id
    } as $tipo_ativo
  
    precondition ($tipo_ativo != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    var $safe_tipo_ativo {
      value = {
        id       : $tipo_ativo.id
        nome     : $tipo_ativo.nome
        descricao: $tipo_ativo.descricao
      }
    }
  }

  response = $safe_tipo_ativo
  guid = "UFSKAoCoHzruWOlNKU_9qoTrjmY"
}