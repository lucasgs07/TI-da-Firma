// Query the interaction and its ticket visibility together so callers cannot
// distinguish an out-of-scope interaction from a missing interaction.
// Return one interaction only when its parent ticket is visible to the authenticated actor.
query "interacao_chamado/{interacao_chamado_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    // Interaction ID from the route.
    int interacao_chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
  
    // Filter by interaction ID and the parent ticket's server-derived visibility scope in the same database read.
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
    
      where = $db.interacao_chamado.id == $input.interacao_chamado_id && (($actor.perfil_id == 1) || ($actor.perfil_id == 2 && ($actor.departamento_id == 1 || $db.requester.departamento_id == $actor.departamento_id)) || ($actor.perfil_id == 3) || ($actor.perfil_id == 4 && $db.ticket.solicitante_id == $actor.id))
      eval = {
        ticket_status_name   : $db.status_chamado.nome
        ticket_responsavel_id: $db.ticket.responsavel_id
      }
    
      return = {type: "single"}
    } as $interaction
  
    precondition ($interaction != null) {
      error_type = "notfound"
      error = "Interaction was not found or is not available."
    }
  
    function.run "helpdesk/access/require_ticket_read" {
      input = {ticket_id: $interaction.chamado_id}
    } as $ticket_read
  
    db.get user {
      field_name = "id"
      field_value = $interaction.user_id
      output = ["id", "name"]
    } as $author
  
    // Return only explicitly approved interaction fields; never include private user data.
    var $public_interaction {
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

  response = $public_interaction
  guid = "Cnw0iYntAzqZDWPmXoZct9uPZdU"
}