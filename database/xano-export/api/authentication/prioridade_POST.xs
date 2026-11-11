// Create a prioridade lookup record; only administrators may mutate lookup data.
query prioridade verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Priority name
    text nome? filters=trim
  
    // Optional priority level
    int nivel?

    // SLA duration in approved working hours, or null when no policy applies.
    int? sla_horas?
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    precondition ($input.sla_horas == null || $input.sla_horas == 12 || $input.sla_horas == 36 || $input.sla_horas == 50) {
      error_type = "inputerror"
      error = "SLA hours must be 12, 36, 50, or null."
    }

    db.add prioridade {
      data = {
        nome     : $input.nome
        nivel    : $input.nivel
        sla_horas: $input.sla_horas
      }
    } as $created_prioridade
  
    var $prioridade {
      value = {
        id       : $created_prioridade.id
        nome     : $created_prioridade.nome
        nivel    : $created_prioridade.nivel
        sla_horas: $created_prioridade.sla_horas
      }
    }
  }

  response = $prioridade
  guid = "Gx68Uat70Taq6G7hiO3XWSxfj6c"
}