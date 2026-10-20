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
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3 || $actor.perfil_id == 4) {
      error_type = "accessdenied"
      error = "Only authenticated operational profiles may access scoped tasks."
    }
  
    function.run "helpdesk/access/task_access" {
      input = {tarefa_id: $input.tarefa_id}
    } as $access
  
    precondition ($access.can_read) {
      error_type = "notfound"
      error = "Task not found or unavailable."
    }
  
    var $tarefa {
      value = $access.task
    }
  }

  response = $tarefa
  guid = "bVz-9_ZmTuPWEsfRg-XsUTa6Djs"
}