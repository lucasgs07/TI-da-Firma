// Get a task only when it is within the authenticated actor's scope.
// Retrieve a task for an administrator, its department manager, or its assigned technician.
query "tarefa/{tarefa_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    // Task ID.
    int tarefa_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "Employees are not allowed to access tasks."
    }
  
    db.get tarefa {
      field_name = "id"
      field_value = $input.tarefa_id
    } as $tarefa
  
    precondition ($tarefa != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    conditional {
      if ($actor.perfil_id == 2) {
        db.get user {
          field_name = "id"
          field_value = $tarefa.responsavel_id
          output = ["id", "perfil_id", "departamento_id"]
        } as $responsavel
      
        precondition ($responsavel != null && $responsavel.perfil_id == 3 && $responsavel.departamento_id == $actor.departamento_id) {
          error_type = "accessdenied"
          error = "Managers may access only tasks assigned to technicians in their department."
        }
      }
    
      elseif ($actor.perfil_id == 3) {
        precondition ($tarefa.responsavel_id == $actor.id) {
          error_type = "accessdenied"
          error = "Technicians may access only tasks assigned to themselves."
        }
      }
    }
  }

  response = $tarefa
  guid = "bVz-9_ZmTuPWEsfRg-XsUTa6Djs"
}