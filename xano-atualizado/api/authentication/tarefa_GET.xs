// List tasks within the authenticated actor's permitted scope.
// List tasks globally for administrators, by assigned technician department for managers, or assigned to the authenticated technician.
query tarefa verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "Employees are not allowed to access tasks."
    }
  
    conditional {
      if ($actor.perfil_id == 1) {
        db.query tarefa {
          return = {type: "list"}
        } as $tarefas
      }
    
      elseif ($actor.perfil_id == 2) {
        db.query user {
          where = $db.user.perfil_id == 3 && $db.user.departamento_id == $actor.departamento_id
          return = {type: "list"}
          output = ["id"]
        } as $department_technicians
      
        var $tarefas {
          value = []
        }
      
        foreach ($department_technicians) {
          each as $technician {
            db.query tarefa {
              where = $db.tarefa.responsavel_id == $technician.id
              return = {type: "list"}
            } as $technician_tarefas
          
            foreach ($technician_tarefas) {
              each as $technician_tarefa {
                array.push $tarefas {
                  value = $technician_tarefa
                }
              }
            }
          }
        }
      }
    
      else {
        db.query tarefa {
          where = $db.tarefa.responsavel_id == $actor.id
          return = {type: "list"}
        } as $tarefas
      }
    }
  }

  response = $tarefas
  guid = "bpl1JPxreXIo7L75WDDxBVPqTWc"
}