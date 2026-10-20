// List tasks within the authenticated actor's permitted scope.
// List tasks globally for administrators, by assigned technician department for managers, or assigned to the authenticated technician.
query tarefa verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3 || $actor.perfil_id == 4) {
      error_type = "accessdenied"
      error = "Only authenticated operational profiles may access scoped tasks."
    }
  
    db.query tarefa {
      sort = {tarefa.created_at: "desc"}
      return = {type: "list"}
      output = ["id"]
    } as $rows
  
    var $tarefas {
      value = []
    }
  
    foreach ($rows) {
      each as $row {
        function.run "helpdesk/access/task_access" {
          input = {tarefa_id: $row.id}
        } as $access
      
        conditional {
          if ($access.can_read) {
            array.push $tarefas {
              value = $access.task
            }
          }
        }
      }
    }
  }

  response = $tarefas
  guid = "bpl1JPxreXIo7L75WDDxBVPqTWc"
}