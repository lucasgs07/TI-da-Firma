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
    int responsavel_id?
  
    // Complete non-empty owner set. Do not combine with the legacy owner field.
    int[] responsaveis_ids?
  
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
  
    var $task_target_profile {
      value = 3
    }
  
    conditional {
      if ($actor.perfil_id == 2 && $actor.departamento_id != 1) {
        var.update $task_target_profile {
          value = 4
        }
      }
    }
  
    var $owner_ids {
      value = []
    }
  
    conditional {
      if ($provided_input|has:"responsaveis_ids") {
        precondition (($provided_input|has:"responsavel_id") == false) {
          error_type = "inputerror"
          error = "Supply either responsaveis_ids or legacy responsavel_id."
        }
      
        precondition ($input.responsaveis_ids != null && ($input.responsaveis_ids|count) > 0) {
          error_type = "inputerror"
          error = "Select at least one responsible user."
        }
      
        var.update $owner_ids {
          value = $input.responsaveis_ids
        }
      }
    
      else {
        precondition ($input.responsavel_id != null && $input.responsavel_id > 0) {
          error_type = "inputerror"
          error = "Select a responsible user."
        }
      
        array.push $owner_ids {
          value = $input.responsavel_id
        }
      }
    }
  
    var $validated_ids {
      value = []
    }
  
    var $first_owner {
      value = null
    }
  
    foreach ($owner_ids) {
      each as $owner_id {
        precondition ($owner_id > 0) {
          error_type = "inputerror"
          error = "Responsible user identifiers must be positive."
        }
      
        function.run "helpdesk/access/authorize_target_user" {
          input = {
            target_user_id    : $owner_id
            expected_perfil_id: $task_target_profile
          }
        } as $valid_owner
      
        array.has ($validated_ids) if ($this == $valid_owner.id) as $already_added
        conditional {
          if ($already_added == false) {
            array.push $validated_ids {
              value = $valid_owner.id
            }
          }
        }
      
        conditional {
          if ($first_owner == null) {
            var.update $first_owner {
              value = $valid_owner.id
            }
          }
        }
      }
    }
  
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
        responsavel_id   : $first_owner
        responsaveis_ids : $validated_ids
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