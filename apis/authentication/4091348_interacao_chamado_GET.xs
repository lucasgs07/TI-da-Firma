// List interactions only for parent tickets visible to the authenticated actor.
// List ticket interactions within the authenticated actor's ticket visibility scope.
query interacao_chamado verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int? chamado_id? filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
  
    // Scope non-technician interactions by parent ticket; technicians have global read access.
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
    
      where = ($input.chamado_id == null || $db.interacao_chamado.chamado_id == $input.chamado_id) && (($actor.perfil_id == 1) || ($actor.perfil_id == 2 && ($actor.departamento_id == 1 || $db.requester.departamento_id == $actor.departamento_id)) || ($actor.perfil_id == 4 && $db.ticket.solicitante_id == $actor.id) || ($actor.perfil_id == 3))
      sort = {
        interacao_chamado.created_at: "asc"
        interacao_chamado.id        : "asc"
      }
    
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
        function.run "helpdesk/access/require_ticket_read" {
          input = {ticket_id: $interaction.chamado_id}
        } as $ticket_read
      
        db.get user {
          field_name = "id"
          field_value = $interaction.user_id
          output = ["id", "name"]
        } as $author
      
        array.push $public_interactions {
          value = {
            id         : $interaction.id
            created_at : $interaction.created_at
            mensagem   : $interaction.mensagem
            chamado_id : $interaction.chamado_id
            user_id    : $interaction.user_id
            author_name: $author.name
          }
        }
      }
    }
  }

  response = $public_interactions
  guid = "UmmSXI_UX8ktXvxfJj9BnOp3qhg"
}