// Create a reply with both its author and parent ticket bound server-side.
// Create an interaction only when the authenticated actor has explicit reply permission on the ticket.
query interacao_chamado verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Parent ticket ID.
    int chamado_id filters=min:1
  
    // Reply message.
    text mensagem filters=trim|min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    db.get chamado {
      field_name = "id"
      field_value = $input.chamado_id
      output = ["id", "solicitante_id", "responsavel_id"]
    } as $ticket
  
    precondition ($ticket != null) {
      error_type = "notfound"
      error = "Ticket was not found."
    }
  
    // Reply authorization is independent of read access: only the ticket's requester or its assigned technician may create a reply.
    var $can_reply {
      value = false
    }
  
    conditional {
      if (($actor.perfil_id == 2 || $actor.perfil_id == 4) && $ticket.solicitante_id == $actor.id) {
        var.update $can_reply {
          value = true
        }
      }
    
      elseif ($actor.perfil_id == 3) {
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
          if ($actor_is_assigned || ($assignment_count == 0 && $ticket.responsavel_id == $actor.id)) {
            var.update $can_reply {
              value = true
            }
          }
        }
      }
    }
  
    precondition ($can_reply) {
      error_type = "accessdenied"
      error = "You are not authorized to reply to this ticket."
    }
  
    db.add interacao_chamado {
      data = {
        created_at: now
        mensagem  : $input.mensagem
        chamado_id: $ticket.id
        user_id   : $actor.id
      }
    } as $created_interaction
  
    // Return only the newly created interaction's approved fields.
    var $public_interaction {
      value = {
        id        : $created_interaction.id
        created_at: $created_interaction.created_at
        mensagem  : $created_interaction.mensagem
        chamado_id: $ticket.id
        user_id   : $actor.id
      }
    }
  }

  response = $public_interaction
  guid = "ngTcjkI10d5sev68ft8KQqDVqQ8"
}