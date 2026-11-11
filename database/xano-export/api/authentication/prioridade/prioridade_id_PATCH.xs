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

    // SLA duration in approved working hours, or null when no policy applies.
    int? sla_horas?
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
  
    conditional {
      if ($raw_input.body|has:"sla_horas") {
        precondition ($input.sla_horas == null || $input.sla_horas == 12 || $input.sla_horas == 36 || $input.sla_horas == 50) {
          error_type = "inputerror"
          error = "SLA hours must be 12, 36, 50, or null."
        }

        var.update $patch {
          value = $patch|set:"sla_horas":$input.sla_horas
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
        id       : $updated_prioridade.id
        nome     : $updated_prioridade.nome
        nivel    : $updated_prioridade.nivel
        sla_horas: $updated_prioridade.sla_horas
      }
    }
  }

  response = $prioridade
  guid = "-c8QGDSKVfUpuLpYYk1FLz473-c"
}