// Update only supplied writable departamento fields; only administrators may mutate lookup data.
query "departamento/{departamento_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int departamento_id filters=min:1
  
    // Department name
    text nome? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get departamento {
      field_name = "id"
      field_value = $input.departamento_id
    } as $existing_departamento
  
    precondition ($existing_departamento != null) {
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
  
    db.patch departamento {
      field_name = "id"
      field_value = $input.departamento_id
      data = $patch
    } as $updated_departamento
  
    var $departamento {
      value = {
        id  : $updated_departamento.id
        nome: $updated_departamento.nome
      }
    }
  }

  response = $departamento
}