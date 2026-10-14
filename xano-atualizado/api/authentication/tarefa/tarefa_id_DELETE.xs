// Administrators delete any task; managers delete tasks assigned to technicians of their department.
// Delete a task as an administrator or as a manager within the manager's department.
query "tarefa/{tarefa_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    // Task ID.
    int tarefa_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Only administrators and managers may delete tasks."
    }
  
    db.get tarefa {
      field_name = "id"
      field_value = $input.tarefa_id
      output = ["id", "responsavel_id"]
    } as $tarefa
  
    precondition ($tarefa != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    conditional {
      if ($actor.perfil_id == 2) {
        db.query user {
          where = $db.user.id == $tarefa.responsavel_id && $db.user.perfil_id == 3 && $db.user.departamento_id == $actor.departamento_id
          return = {type: "single"}
          output = ["id"]
        } as $scoped_owner
      
        precondition ($scoped_owner != null) {
          error_type = "notfound"
          error = "Task not found."
        }
      }
    }
  
    db.del tarefa {
      field_name = "id"
      field_value = $tarefa.id
    }
  }

  response = {success: true}
  guid = "-5EWMt48YP-dkxhOPx2wWQkT8ZI"
}