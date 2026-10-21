// Update only supplied writable tipo_ativo fields; only administrators may mutate lookup data.
query "tipo_ativo/{tipo_ativo_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int tipo_ativo_id filters=min:1
  
    // Asset type name
    text nome? filters=trim
  
    // Optional asset type description
    text? descricao? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get tipo_ativo {
      field_name = "id"
      field_value = $input.tipo_ativo_id
    } as $existing_tipo_ativo
  
    precondition ($existing_tipo_ativo != null) {
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
  
    db.patch tipo_ativo {
      field_name = "id"
      field_value = $input.tipo_ativo_id
      data = $patch
    } as $updated_tipo_ativo
  
    var $tipo_ativo {
      value = {
        id       : $updated_tipo_ativo.id
        nome     : $updated_tipo_ativo.nome
        descricao: $updated_tipo_ativo.descricao
      }
    }
  }

  response = $tipo_ativo
}