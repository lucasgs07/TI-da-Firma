// Update only supplied writable status_ativo fields; only administrators may mutate lookup data.
query "status_ativo/{status_ativo_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int status_ativo_id filters=min:1
  
    // Asset status name
    text nome? filters=trim
  
    // Optional asset status description
    text? descricao? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get status_ativo {
      field_name = "id"
      field_value = $input.status_ativo_id
    } as $existing_status_ativo
  
    precondition ($existing_status_ativo != null) {
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
      if ($raw_input.body|has:"descricao") {
        var.update $patch {
          value = $patch|set:"descricao":$input.descricao
        }
      }
    }
  
    precondition (($patch|count) > 0) {
      error_type = "inputerror"
      error = "At least one writable field must be supplied."
    }
  
    db.patch status_ativo {
      field_name = "id"
      field_value = $input.status_ativo_id
      data = $patch
    } as $updated_status_ativo
  
    var $status_ativo {
      value = {
        id       : $updated_status_ativo.id
        nome     : $updated_status_ativo.nome
        descricao: $updated_status_ativo.descricao
      }
    }
  }

  response = $status_ativo
  guid = "3lcFB6WHOHJ1K4tL0dQnp_DqTzc"
}