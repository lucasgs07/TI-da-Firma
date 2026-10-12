// Update only supplied writable status_chamado fields; only administrators may mutate lookup data.
query "status_chamado/{status_chamado_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int status_chamado_id filters=min:1
  
    // Ticket status name
    text nome? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get status_chamado {
      field_name = "id"
      field_value = $input.status_chamado_id
    } as $existing_status_chamado
  
    precondition ($existing_status_chamado != null) {
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
  
    precondition (($patch|count) > 0) {
      error_type = "inputerror"
      error = "At least one writable field must be supplied."
    }
  
    db.patch status_chamado {
      field_name = "id"
      field_value = $input.status_chamado_id
      data = $patch
    } as $updated_status_chamado
  
    var $status_chamado {
      value = {
        id  : $updated_status_chamado.id
        nome: $updated_status_chamado.nome
      }
    }
  }

  response = $status_chamado
  guid = "m9o1ZWHaqgRQQLdhkfXvPseF4ks"
}