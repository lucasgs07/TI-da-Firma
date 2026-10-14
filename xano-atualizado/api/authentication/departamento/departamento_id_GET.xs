// Get a safe departamento lookup record.
query "departamento/{departamento_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int departamento_id filters=min:1
  }

  stack {
    db.get departamento {
      field_name = "id"
      field_value = $input.departamento_id
    } as $departamento
  
    precondition ($departamento != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    var $safe_departamento {
      value = {id: $departamento.id, nome: $departamento.nome}
    }
  }

  response = $safe_departamento
  guid = "xMuIZ8vsx3L8GomblzX1V44ta2M"
}