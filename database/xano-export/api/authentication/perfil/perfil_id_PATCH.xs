// Update only supplied writable perfil fields; only administrators may mutate lookup data.
query "perfil/{perfil_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int perfil_id filters=min:1
  
    // Profile name
    text name? filters=trim
  
    // Optional profile description
    text? descricao? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get perfil {
      field_name = "id"
      field_value = $input.perfil_id
    } as $existing_perfil
  
    precondition ($existing_perfil != null) {
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
      if ($raw_input.body|has:"name") {
        var.update $patch {
          value = $patch|set:"name":$input.name
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
  
    db.patch perfil {
      field_name = "id"
      field_value = $input.perfil_id
      data = $patch
    } as $updated_perfil
  
    var $perfil {
      value = {
        id       : $updated_perfil.id
        name     : $updated_perfil.name
        descricao: $updated_perfil.descricao
      }
    }
  }

  response = $perfil
  guid = "9DURbm74ooePh7oGGmf4NQ80su8"
}