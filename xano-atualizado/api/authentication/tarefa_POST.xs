// Create a task and derive the requester from the authenticated actor.
// Create and assign a task globally as an administrator or within the manager's department.
query tarefa verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Task title.
    text titulo filters=trim|min:1
  
    // Optional task description.
    text descricao? filters=trim
  
    // Optional due date.
    date prazo?
  
    // User ID of the technician assigned to the task.
    int responsavel_id filters=min:1
  
    // Optional related ticket ID.
    int chamado_id?
  
    // Existing task priority ID.
    int prioridade_id filters=min:1
  
    // Reserved for rejection: requester identity is always derived from the authenticated actor.
    int solicitante_id?
  
    // Reserved for rejection: task status is initialized by the server.
    int status_chamado_id?
  
    // Reserved for rejection: task status is initialized by the server.
    text status_nome? filters=trim
  
    // Reserved for rejection: task status is initialized by the server.
    text status? filters=trim
  
    // Reserved for rejection: task completion/solution is not enabled in this batch.
    text solucao_aplicada? filters=trim
  }

  stack {
    util.get_all_input as $provided_input
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Only administrators and managers may create tasks."
    }
  
    conditional {
      if ($provided_input|has:"solicitante_id" || $provided_input|has:"status_chamado_id" || $provided_input|has:"status_nome" || $provided_input|has:"status" || $provided_input|has:"solucao_aplicada") {
        precondition (false) {
          error_type = "inputerror"
          error = "Requester, status, and task completion fields are server-managed and must not be supplied."
        }
      }
    }
  
    var $due_date {
      value = null
    }
  
    var $related_ticket_id {
      value = null
    }
  
    conditional {
      if ($provided_input|has:"prazo") {
        var.update $due_date {
          value = $provided_input.prazo
        }
      }
    }
  
    conditional {
      if ($provided_input.chamado_id > 0) {
        var.update $related_ticket_id {
          value = $provided_input.chamado_id
        }
      }
    }
  
    db.get prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
      output = ["id", "nome"]
    } as $prioridade
  
    precondition ($prioridade != null) {
      error_type = "inputerror"
      error = "The selected task priority does not exist."
    }
  
    function.run "helpdesk/access/authorize_target_user" {
      input = {
        target_user_id    : $input.responsavel_id
        expected_perfil_id: 3
      }
    } as $responsavel
  
    conditional {
      if ($related_ticket_id != null) {
        conditional {
          if ($actor.perfil_id == 2) {
            function.run "helpdesk/access/require_ticket_read" {
              input = {ticket_id: $related_ticket_id}
            } as $ticket_access
          }
        
          else {
            db.get chamado {
              field_name = "id"
              field_value = $related_ticket_id
              output = ["id"]
            } as $ticket
          
            precondition ($ticket != null) {
              error_type = "inputerror"
              error = "The related ticket does not exist."
            }
          }
        }
      }
    }
  
    db.query status_chamado {
      where = $db.status_chamado.nome == "Aberto"
      return = {type: "single"}
    } as $status_aberto
  
    precondition ($status_aberto != null) {
      error_type = "inputerror"
      error = "The required task status 'Aberto' is not configured."
    }
  
    db.add tarefa {
      data = {
        titulo           : $input.titulo
        descricao        : $input.descricao
        prazo            : $due_date
        solicitante_id   : $actor.id
        responsavel_id   : $responsavel.id
        chamado_id       : $related_ticket_id
        prioridade_id    : $prioridade.id
        status_chamado_id: $status_aberto.id
        created_at       : now
      }
    } as $tarefa
  }

  response = $tarefa
  guid = "fdQ9YGwDWseLlHo45nRK5M9rJNk"
}