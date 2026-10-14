// List interactions only for parent tickets visible to the authenticated actor.
// List ticket interactions within the authenticated actor's ticket visibility scope.
query interacao_chamado verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
  
    // Scope non-technician interactions by parent ticket; technician interactions are filtered against open status and assignment relations below.
    db.query interacao_chamado {
      join = {
        ticket        : {
          table: "chamado"
          where: $db.interacao_chamado.chamado_id == $db.ticket.id
        }
        status_chamado: {
          table: "status_chamado"
          type : "left"
          where: $db.ticket.status_chamado_id == $db.status_chamado.id
        }
        requester     : {
          table: "user"
          type : "left"
          where: $db.ticket.solicitante_id == $db.requester.id
        }
      }
    
      where = ($actor.perfil_id == 1) || ($actor.perfil_id == 2 && ($actor.departamento_id == 1 || $db.ticket.solicitante_id == $actor.id || ($db.requester.perfil_id == 4 && $db.requester.departamento_id == $actor.departamento_id))) || ($actor.perfil_id == 4 && $db.ticket.solicitante_id == $actor.id) || ($actor.perfil_id == 3)
      sort = {interacao_chamado.created_at: "asc"}
      eval = {
        ticket_status_name   : $db.status_chamado.nome
        ticket_responsavel_id: $db.ticket.responsavel_id
      }
    
      return = {type: "list"}
    } as $interactions
  
    // Build an explicit response whitelist and validate each related parent ticket with the shared read helper.
    var $public_interactions {
      value = []
    }
  
    foreach ($interactions) {
      each as $interaction {
        var $can_include_interaction {
          value = ($actor.perfil_id != 3)
        }
      
        conditional {
          if ($actor.perfil_id == 3) {
            db.query chamado_tecnico {
              where = $db.chamado_tecnico.chamado_id == $interaction.chamado_id
              return = {type: "list"}
            } as $interaction_ticket_assignments
          
            var $interaction_assignment_count {
              value = $interaction_ticket_assignments|count
            }
          
            var $actor_is_assigned {
              value = false
            }
          
            db.query chamado_tecnico {
              where = $db.chamado_tecnico.chamado_id == $interaction.chamado_id && $db.chamado_tecnico.tecnico_id == $actor.id
              return = {type: "single"}
            } as $actor_ticket_assignment
          
            var.update $actor_is_assigned {
              value = ($actor_ticket_assignment != null)
            }
          
            conditional {
              if ($interaction.ticket_status_name == "Aberto" || $actor_is_assigned || ($interaction_assignment_count == 0 && $interaction.ticket_responsavel_id == $actor.id)) {
                var.update $can_include_interaction {
                  value = true
                }
              }
            }
          }
        
          else {
            function.run "helpdesk/access/require_ticket_read" {
              input = {ticket_id: $interaction.chamado_id}
            } as $ticket_read
          }
        }
      
        conditional {
          if ($can_include_interaction) {
            array.push $public_interactions {
              value = {
                id        : $interaction.id
                created_at: $interaction.created_at
                mensagem  : $interaction.mensagem
                chamado_id: $interaction.chamado_id
                user_id   : $interaction.user_id
              }
            }
          }
        }
      }
    }
  }

  response = $public_interactions
  guid = "UmmSXI_UX8ktXvxfJj9BnOp3qhg"
}