// Only the assigned technician may update a ticket's operation.
// Allow the assigned technician to update operational status and final solution.
query "chamado/{chamado_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    // Ticket ID from the route; retained for route compatibility.
    int chamado_id filters=min:1
  
    // Operational status name. Allowed: Em Análise, Em atendimento, Aguardando usuário, Resolvido, or Fechado.
    text status_nome? filters=trim|max:50
  
    // Final resolution text. Required in the same request when moving the ticket to Resolvido or Fechado.
    text solucao_final? filters=trim|max:5000
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "Only technicians may change ticket operations."
    }
  
    db.get chamado {
      field_name = "id"
      field_value = $input.chamado_id
      output = [
        "id"
        "titulo"
        "descricao"
        "solucao_final"
        "status_chamado_id"
        "categoria_chamado_id"
        "prioridade_id"
        "solicitante_id"
        "responsavel_id"
        "atualizado_em"
        "resolvido_em"
      ]
    } as $ticket
  
    precondition ($ticket != null) {
      error_type = "notfound"
      error = "Ticket was not found."
    }
  
    precondition ($input.status_nome == null || $input.status_nome == "Em Análise" || $input.status_nome == "Em atendimento" || $input.status_nome == "Aguardando usuário" || $input.status_nome == "Resolvido" || $input.status_nome == "Fechado") {
      error_type = "inputerror"
      error = "The requested ticket status is not allowed."
    }
  
    precondition ($input.status_nome != null || $input.solucao_final != null) {
      error_type = "inputerror"
      error = "Provide an operational status or a final solution to update."
    }
  
    db.query chamado_tecnico {
      where = $db.chamado_tecnico.chamado_id == $ticket.id
      return = {type: "list"}
    } as $ticket_assignments
  
    var $assignment_count {
      value = $ticket_assignments|count
    }
  
    var $actor_is_assigned {
      value = false
    }
  
    db.query chamado_tecnico {
      where = $db.chamado_tecnico.chamado_id == $ticket.id && $db.chamado_tecnico.tecnico_id == $actor.id
      return = {type: "single"}
    } as $actor_ticket_assignment
  
    var.update $actor_is_assigned {
      value = ($actor_ticket_assignment != null)
    }
  
    conditional {
      if ($assignment_count > 0) {
        precondition ($actor_is_assigned) {
          error_type = "accessdenied"
          error = "Only an assigned technician may update this ticket."
        }
      }
    
      else {
        precondition ($ticket.responsavel_id == $actor.id) {
          error_type = "accessdenied"
          error = "Only the legacy assigned technician may update this ticket."
        }
      }
    }
  
    precondition ($ticket.status_chamado_id != null) {
      error = "The ticket status could not be verified."
    }
  
    db.get status_chamado {
      field_name = "id"
      field_value = $ticket.status_chamado_id
      output = ["id", "nome"]
    } as $current_status
  
    precondition ($current_status != null) {
      error = "The ticket status could not be verified."
    }
  
    precondition ($current_status.nome == "Aberto" || $current_status.nome == "Em Análise" || $current_status.nome == "Em atendimento" || $current_status.nome == "Aguardando usuário" || $current_status.nome == "Resolvido" || $current_status.nome == "Fechado") {
      error_type = "accessdenied"
      error = "This status is not valid for ticket operations."
    }
  
    precondition (($current_status.nome != "Resolvido") && ($current_status.nome != "Fechado")) {
      error_type = "accessdenied"
      error = "Resolved or closed tickets cannot be changed."
    }
  
    // Build an explicit write whitelist; caller-supplied ownership, requester, category, title, and priority fields are never accepted.
    var $patch_data {
      value = {atualizado_em: now}
    }
  
    conditional {
      if ($input.status_nome != null) {
        db.get status_chamado {
          field_name = "nome"
          field_value = $input.status_nome
          output = ["id", "nome"]
        } as $requested_status
      
        precondition ($requested_status != null) {
          error_type = "inputerror"
          error = "The requested ticket status is not configured."
        }
      
        conditional {
          if ($input.status_nome == "Resolvido" || $input.status_nome == "Fechado") {
            precondition ($input.solucao_final != null && ($input.solucao_final|strlen) > 0) {
              error_type = "inputerror"
              error = "A non-empty final solution is required to resolve or close a ticket."
            }
          
            var.update $patch_data {
              value = $patch_data
                |set:"status_chamado_id":$requested_status.id
                |set:"resolvido_em":now
            }
          }
        
          else {
            var.update $patch_data {
              value = $patch_data
                |set:"status_chamado_id":$requested_status.id
            }
          }
        }
      }
    }
  
    conditional {
      if ($input.solucao_final != null) {
        precondition (($input.solucao_final|strlen) > 0) {
          error_type = "inputerror"
          error = "The final solution cannot be empty."
        }
      
        var.update $patch_data {
          value = $patch_data
            |set:"solucao_final":$input.solucao_final
        }
      }
    }
  
    db.patch chamado {
      field_name = "id"
      field_value = $input.chamado_id
      data = $patch_data
    } as $updated_ticket
  
    db.get chamado {
      field_name = "id"
      field_value = $input.chamado_id
      output = [
        "id"
        "titulo"
        "descricao"
        "solucao_final"
        "status_chamado_id"
        "categoria_chamado_id"
        "prioridade_id"
        "solicitante_id"
        "responsavel_id"
        "atualizado_em"
        "resolvido_em"
      ]
    } as $saved_ticket
  
    precondition ($saved_ticket != null) {
      error_type = "notfound"
      error = "Ticket was not found after the update."
    }
  
    db.get status_chamado {
      field_name = "id"
      field_value = $saved_ticket.status_chamado_id
      output = ["id", "nome"]
    } as $saved_status
  
    // Return only the approved public ticket fields.
    var $public_ticket {
      value = {
        id                  : $saved_ticket.id
        titulo              : $saved_ticket.titulo
        descricao           : $saved_ticket.descricao
        solucao_final       : $saved_ticket.solucao_final
        status_chamado_id   : $saved_ticket.status_chamado_id
        status_nome         : $saved_status.nome
        categoria_chamado_id: $saved_ticket.categoria_chamado_id
        prioridade_id       : $saved_ticket.prioridade_id
        solicitante_id      : $saved_ticket.solicitante_id
        responsavel_id      : $saved_ticket.responsavel_id
        atualizado_em       : $saved_ticket.atualizado_em
        resolvido_em        : $saved_ticket.resolvido_em
      }
    }
  }

  response = $public_ticket
  guid = "7HZCLLmByxoZgyfx4ix-kC8-1WE"
}