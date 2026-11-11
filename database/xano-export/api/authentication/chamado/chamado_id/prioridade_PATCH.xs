// Change a ticket priority and recalculate its SLA within the authenticated manager scope.
query "chamado/{chamado_id}/prioridade" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int chamado_id filters=min:1
    int prioridade_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Only managers and administrators may change ticket priority."
    }
  
    db.query chamado {
      join = {
        requester: {
          table: "user"
          type : "left"
          where: $db.chamado.solicitante_id == $db.requester.id
        }
      }
      where = $db.chamado.id == $input.chamado_id && ($actor.perfil_id == 1 || ($actor.perfil_id == 2 && ($actor.departamento_id == 1 || $db.chamado.solicitante_id == $actor.id || ($db.requester.perfil_id == 4 && $db.requester.departamento_id == $actor.departamento_id))))
      return = {type: "single"}
    } as $ticket
  
    precondition ($ticket != null) {
      error_type = "notfound"
      error = "Ticket was not found or is not available."
    }
  
    precondition ($ticket.prioridade_id != $input.prioridade_id) {
      error_type = "inputerror"
      error = "The requested priority is already set."
    }
  
    db.get prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
      output = ["id", "nome", "sla_horas"]
    } as $priority
  
    precondition ($priority != null) {
      error_type = "inputerror"
      error = "The selected priority does not exist."
    }
  
    var $sla_dates {
      value = {sla_inicio_em: null, prazo_sla: null}
    }
  
    conditional {
      if ($priority.sla_horas != null) {
        function.run "helpdesk/sla/calculate_deadline" {
          input = {
            start_at : now
            sla_horas: $priority.sla_horas
          }
        } as $calculated_sla
      
        var.update $sla_dates {
          value = $calculated_sla
        }
      }
    }
  
    db.patch chamado {
      field_name = "id"
      field_value = $ticket.id
      data = {
        prioridade_id : $priority.id
        sla_inicio_em : $sla_dates.sla_inicio_em
        prazo_sla     : $sla_dates.prazo_sla
        atualizado_em : now
      }
    } as $updated_ticket
  
    precondition ($updated_ticket != null) {
      error_type = "notfound"
      error = "Ticket was not found after the update."
    }
  
    var $response {
      value = {
        id             : $updated_ticket.id
        prioridade_id  : $updated_ticket.prioridade_id
        prioridade_nome: $priority.nome
        sla_horas      : $priority.sla_horas
        sla_inicio_em  : $updated_ticket.sla_inicio_em
        prazo_sla      : $updated_ticket.prazo_sla
        atualizado_em  : $updated_ticket.atualizado_em
      }
    }
  }

  response = $response
}
