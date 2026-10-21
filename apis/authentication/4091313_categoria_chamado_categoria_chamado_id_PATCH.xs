// Update only supplied writable categoria_chamado fields; only administrators may mutate lookup data.
query "categoria_chamado/{categoria_chamado_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int categoria_chamado_id filters=min:1
  
    // Ticket category name
    text nome? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get categoria_chamado {
      field_name = "id"
      field_value = $input.categoria_chamado_id
    } as $existing_categoria_chamado
  
    precondition ($existing_categoria_chamado != null) {
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
  
    db.patch categoria_chamado {
      field_name = "id"
      field_value = $input.categoria_chamado_id
      data = $patch
    } as $updated_categoria_chamado
  
    var $categoria_chamado {
      value = {
        id  : $updated_categoria_chamado.id
        nome: $updated_categoria_chamado.nome
      }
    }
  }

  response = $categoria_chamado
}