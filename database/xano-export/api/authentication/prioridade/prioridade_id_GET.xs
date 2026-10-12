// Get a safe prioridade lookup record.
query "prioridade/{prioridade_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int prioridade_id filters=min:1
  }

  stack {
    db.get prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
    } as $prioridade
  
    precondition ($prioridade != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    var $safe_prioridade {
      value = {
        id   : $prioridade.id
        nome : $prioridade.nome
        nivel: $prioridade.nivel
      }
    }
  }

  response = $safe_prioridade
  guid = "l3fU1XRQcjVzjcP3dz5e-SCAkKk"
}