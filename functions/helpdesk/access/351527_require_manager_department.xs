// Require a manager and return the manager's trusted department scope, including the TI global read-only ticket exception.
function "helpdesk/access/require_manager_department" {
  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" {
      mock = {
        "should return the authenticated manager department scope" : {id: 21, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should identify the TI manager global read-only exception": {id: 22, name: "TI Manager", perfil_id: 2, departamento_id: 1}
        "should deny a non-manager department scope request"       : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
      }
    } as $actor
  
    precondition ($actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Manager access is required."
    }
  
    precondition ($actor.departamento_id != null) {
      error_type = "accessdenied"
      error = "A manager must belong to a department."
    }
  
    // Department identity comes from the authenticated user record, not caller-supplied input.
    var $manager_scope {
      value = {
        actor_id                                          : $actor.id
        departamento_id                                   : $actor.departamento_id
        is_ti_manager                                     : $actor.departamento_id == 1
        ticket_scope                                      : ($actor.departamento_id == 1) ? "global_read_only" : "own_and_department_employee_read_only"
        tickets_read_only                                 : true
        can_create_technicians_and_employees_in_department: true
        can_create_tasks_in_department                    : true
      }
    }
  }

  response = $manager_scope

  test "should return the authenticated manager department scope" {
    expect.to_equal ($response.departamento_id) {
      value = 7
    }
  
    expect.to_equal ($response.ticket_scope) {
      value = "own_and_department_employee_read_only"
    }
  
    expect.to_be_true ($response.can_create_tasks_in_department)
  }

  test "should identify the TI manager global read-only exception" {
    expect.to_equal ($response.departamento_id) {
      value = 1
    }
  
    expect.to_be_true ($response.is_ti_manager)
    expect.to_equal ($response.ticket_scope) {
      value = "global_read_only"
    }
  }

  test "should deny a non-manager department scope request" {
    expect.to_throw {
      exception = ""
    }
  }
}