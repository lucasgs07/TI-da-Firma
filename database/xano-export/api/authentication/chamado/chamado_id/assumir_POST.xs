// Let an authenticated technician join an open ticket without replacing any other assignment.
// Assign the authenticated technician to an open ticket; relation rows support multiple technicians.
query "chamado/{chamado_id}/assumir" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Ticket ID from the route.
    int chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "Only technicians may self-assign tickets."
    }
  
    db.get status_chamado {
      field_name = "nome"
      field_value = "Aberto"
      output = ["id"]
    } as $open_status
  
    precondition ($open_status != null) {
      error = "The configured open ticket status could not be found."
    }
  
    db.query chamado {
      where = $db.chamado.id == $input.chamado_id && $db.chamado.status_chamado_id == $open_status.id
      return = {type: "single"}
      output = ["id", "responsavel_id"]
    } as $claimable
  
    precondition ($claimable != null) {
      error_type = "notfound"
      error = "Ticket was not found or is not open."
    }
  
    db.query chamado_tecnico {
      where = $db.chamado_tecnico.chamado_id == $claimable.id && $db.chamado_tecnico.tecnico_id == $claimable.responsavel_id
      return = {type: "single"}
    } as $legacy_assignment
  
    conditional {
      if ($claimable.responsavel_id != null && $legacy_assignment == null && $claimable.responsavel_id != $actor.id) {
        db.get user {
          field_name = "id"
          field_value = $claimable.responsavel_id
          output = ["id", "perfil_id"]
        } as $legacy_owner
      
        precondition ($legacy_owner != null && $legacy_owner.perfil_id == 3) {
          error = "The ticket's legacy owner cannot be migrated to the technician assignment list."
        }
      
        try_catch {
          try {
            db.add chamado_tecnico {
              data = {chamado_id: $claimable.id, tecnico_id: $legacy_owner.id}
            } as $migrated_legacy_assignment
          }
        
          catch {
            db.query chamado_tecnico {
              where = $db.chamado_tecnico.chamado_id == $claimable.id && $db.chamado_tecnico.tecnico_id == $legacy_owner.id
              return = {type: "single"}
            } as $confirmed_legacy_assignment
          
            precondition ($confirmed_legacy_assignment != null) {
              error = "The ticket's legacy technician could not be preserved. Retry; if it persists, contact an administrator."
            }
          }
        }
      }
    }
  
    db.query chamado_tecnico {
      where = $db.chamado_tecnico.chamado_id == $claimable.id && $db.chamado_tecnico.tecnico_id == $actor.id
      return = {type: "single"}
    } as $existing_assignment
  
    conditional {
      if ($existing_assignment == null) {
        try_catch {
          try {
            db.add chamado_tecnico {
              data = {chamado_id: $claimable.id, tecnico_id: $actor.id}
            } as $new_assignment
          }
        
          catch {
            // A concurrent request by this same technician may have won the unique-index race.
            db.query chamado_tecnico {
              where = $db.chamado_tecnico.chamado_id == $claimable.id && $db.chamado_tecnico.tecnico_id == $actor.id
              return = {type: "single"}
            } as $assignment_after_error
          
            precondition ($assignment_after_error != null) {
              error = "Technician assignment could not be completed. Retry; if it persists, contact an administrator."
            }
          }
        }
      }
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
    } as $claimed_ticket
  
    db.query chamado_tecnico {
      where = $db.chamado_tecnico.chamado_id == $input.chamado_id && $db.chamado_tecnico.tecnico_id == $actor.id
      return = {type: "single"}
    } as $confirmed_assignment
  
    precondition ($claimed_ticket != null && $confirmed_assignment != null) {
      error_type = "notfound"
      error = "Ticket was not found or is not available."
    }
  
    // Return an explicit ticket-field whitelist and no user records or secrets.
    var $public_ticket {
      value = {
        id                  : $claimed_ticket.id
        titulo              : $claimed_ticket.titulo
        descricao           : $claimed_ticket.descricao
        solucao_final       : $claimed_ticket.solucao_final
        status_chamado_id   : $claimed_ticket.status_chamado_id
        status_nome         : "Aberto"
        categoria_chamado_id: $claimed_ticket.categoria_chamado_id
        prioridade_id       : $claimed_ticket.prioridade_id
        solicitante_id      : $claimed_ticket.solicitante_id
        responsavel_id      : $claimed_ticket.responsavel_id
        atualizado_em       : $claimed_ticket.atualizado_em
        resolvido_em        : $claimed_ticket.resolvido_em
      }
    }
  }

  response = $public_ticket
  guid = "eSDXh8Hi4yHba_dG5e1fhYKEeuA"
}