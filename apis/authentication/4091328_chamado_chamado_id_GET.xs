// Fetch one ticket only when it satisfies the authenticated actor's list scope.
// Return a safe ticket view only when the authenticated actor may read it.
query "chamado/{chamado_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    // Ticket ID from the route.
    int chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
  
    // Combine the requested ID and visibility scope in the same database query to conceal out-of-scope records.
    db.query chamado {
      join = {
        requester    : {
          table: "user"
          type : "left"
          where: $db.chamado.solicitante_id == $db.requester.id
        }
        responsible  : {
          table: "user"
          type : "left"
          where: $db.chamado.responsavel_id == $db.responsible.id
        }
        category     : {
          table: "categoria_chamado"
          type : "left"
          where: $db.chamado.categoria_chamado_id == $db.category.id
        }
        priority     : {
          table: "prioridade"
          type : "left"
          where: $db.chamado.prioridade_id == $db.priority.id
        }
        ticket_status: {
          table: "status_chamado"
          type : "left"
          where: $db.chamado.status_chamado_id == $db.ticket_status.id
        }
      }
    
      where = $db.chamado.id == $input.chamado_id && (($actor.perfil_id == 1) || ($actor.perfil_id == 2 && ($actor.departamento_id == 1 || $db.chamado.solicitante_id == $actor.id || ($db.requester.perfil_id == 4 && $db.requester.departamento_id == $actor.departamento_id))) || ($actor.perfil_id == 3) || ($actor.perfil_id == 4 && $db.chamado.solicitante_id == $actor.id))
      eval = {
        requester_name  : $db.requester.name
        responsible_name: $db.responsible.name
        category_name   : $db.category.nome
        priority_name   : $db.priority.nome
        status_name     : $db.ticket_status.nome
      }
    
      return = {type: "single"}
    } as $ticket
  
    precondition ($ticket != null) {
      error_type = "notfound"
      error = "Ticket was not found or is not available."
    }
  
    db.query chamado_tecnico {
      where = $db.chamado_tecnico.chamado_id == $ticket.id
      return = {type: "list"}
    } as $ticket_assignments
  
    var $assignment_count {
      value = $ticket_assignments|count
    }
  
    var $assigned_technicians {
      value = []
    }
  
    foreach ($ticket_assignments) {
      each as $assignment {
        db.get user {
          field_name = "id"
          field_value = $assignment.tecnico_id
          output = ["id", "name"]
        } as $assigned_user
      
        conditional {
          if ($assigned_user != null) {
            array.push $assigned_technicians {
              value = {id: $assigned_user.id, name: $assigned_user.name}
            }
          }
        }
      }
    }
  
    conditional {
      if ($assignment_count == 0 && $ticket.responsavel_id != null) {
        db.get user {
          field_name = "id"
          field_value = $ticket.responsavel_id
          output = ["id", "name"]
        } as $legacy_responsible
      
        conditional {
          if ($legacy_responsible != null) {
            array.push $assigned_technicians {
              value = {
                id  : $legacy_responsible.id
                name: $legacy_responsible.name
              }
            }
          }
        }
      }
    }
  
    // Whitelist public ticket fields; user credentials and private user columns are never returned.
    var $public_ticket {
      value = {
        id                  : $ticket.id
        titulo              : $ticket.titulo
        descricao           : $ticket.descricao
        solucao_final       : $ticket.solucao_final
        status_chamado_id   : $ticket.status_chamado_id
        status_name         : $ticket.status_name
        categoria_chamado_id: $ticket.categoria_chamado_id
        category_name       : $ticket.category_name
        prioridade_id       : $ticket.prioridade_id
        priority_name       : $ticket.priority_name
        solicitante_id      : $ticket.solicitante_id
        requester_name      : $ticket.requester_name
        responsavel_id      : $ticket.responsavel_id
        responsible_name    : $ticket.responsible_name
        tecnicos            : $assigned_technicians
        atualizado_em       : $ticket.atualizado_em
        resolvido_em        : $ticket.resolvido_em
      }
    }
  }

  response = $public_ticket
  guid = "KBn_nHmcgSq4AVSXT9jTanXHORk"
}