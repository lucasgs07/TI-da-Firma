// Update only supplied writable prioridade fields; only administrators may mutate lookup data.
query "prioridade/{prioridade_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int prioridade_id filters=min:1
  
    // Priority name
    text nome? filters=trim
  
    // Priority level
    int nivel?
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
    } as $existing_prioridade
  
    precondition ($existing_prioridade != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    util.get_raw_input {
      encoding = "json"
      exclude_middleware = false
    } as $raw_input
  
    var $patch {
      value = {}
    }
  
    conditional {
      if ($raw_input.body|has:"nome") {
        var.update $patch {
          value = $patch|set:"nome":$input.nome
        }
      }
    }
  
    conditional {
      if ($raw_input.body|has:"nivel") {
        var.update $patch {
          value = $patch|set:"nivel":$input.nivel
        }
      }
    }
  
    precondition (($patch|count) > 0) {
      error_type = "inputerror"
      error = "At least one writable field must be supplied."
    }
  
    db.patch prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
      data = $patch
    } as $updated_prioridade
  
    var $prioridade {
      value = {
        id   : $updated_prioridade.id
        nome : $updated_prioridade.nome
        nivel: $updated_prioridade.nivel
      }
    }
  }

  response = $prioridade
}