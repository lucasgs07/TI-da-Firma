// Return server-derived ticket and task scope hints for the authenticated profile; callers must still apply these scopes in database queries.
function "helpdesk/access/get_actor_scope" {
  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" {
      mock = {
        "should return administrator global scopes and creation permissions": {id: 10, name: "Admin", perfil_id: 1, departamento_id: 7}
        "should return TI manager department scope and creation permissions": {id: 20, name: "TI Manager", perfil_id: 2, departamento_id: 1}
        "should return non-TI manager employee-request scope"               : {id: 21, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should return technician queue and assigned task scopes"           : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should return employee requester-only scope"                       : {id: 40, name: "Employee", perfil_id: 4, departamento_id: 7}
      }
    } as $actor
  
    // Explicit per-profile visibility and creation scope for subsequent API batches.
    var $scope {
      value = {
        actor_id                                          : $actor.id
        perfil_id                                         : $actor.perfil_id
        departamento_id                                   : $actor.departamento_id
        ticket_scope                                      : ""
        ticket_read_only                                  : false
        ticket_scope_includes_open_queue                  : false
        ticket_scope_includes_actor_assigned              : false
        ticket_scope_includes_actor_requested             : false
        ticket_scope_includes_department_employee_requests: false
        task_scope                                        : ""
        can_create_tickets                                : false
        can_create_users_globally                         : false
        can_create_users_in_department                    : false
        can_create_tasks_in_department                    : false
        can_create_tasks_globally                         : false
        can_create_technicians_or_employees_in_department : false
      }
    }
  
    switch ($actor.perfil_id) {
      case (1) {
        var.update $scope {
          value = $scope
            |set:"ticket_scope":"all"
            |set:"task_scope":"all"
            |set:"can_create_users_globally":true
            |set:"can_create_tasks_globally":true
        }
      } break
    
      case (2) {
        conditional {
          if ($actor.departamento_id == 1) {
            var.update $scope {
              value = $scope
                |set:"ticket_scope":"global_read_only"
                |set:"ticket_read_only":true
                |set:"task_scope":"own_department"
                |set:"can_create_tickets":true
                |set:"can_create_users_in_department":true
                |set:"can_create_tasks_in_department":true
                |set:"can_create_technicians_or_employees_in_department":true
            }
          }
        
          else {
            var.update $scope {
              value = $scope
                |set:"ticket_scope":"own_and_department_employee_requests_read_only"
                |set:"ticket_read_only":true
                |set:"ticket_scope_includes_actor_requested":true
                |set:"ticket_scope_includes_department_employee_requests":true
                |set:"task_scope":"own_department"
                |set:"can_create_tickets":true
                |set:"can_create_users_in_department":true
                |set:"can_create_tasks_in_department":true
                |set:"can_create_technicians_or_employees_in_department":true
            }
          }
        }
      } break
    
      case (3) {
        var.update $scope {
          value = $scope
            |set:"ticket_scope":"open_queue_or_actor_assigned"
            |set:"ticket_scope_includes_open_queue":true
            |set:"ticket_scope_includes_actor_assigned":true
            |set:"task_scope":"actor_assigned"
        }
      } break
    
      case (4) {
        var.update $scope {
          value = $scope
            |set:"ticket_scope":"actor_requested"
            |set:"ticket_read_only":true
            |set:"ticket_scope_includes_actor_requested":true
            |set:"task_scope":"none"
            |set:"can_create_tickets":true
        }
      } break
    }
  }

  response = $scope

  test "should return administrator global scopes and creation permissions" {
    expect.to_equal ($response) {
      value = {
        actor_id                                          : 10
        perfil_id                                         : 1
        departamento_id                                   : 7
        ticket_scope                                      : "all"
        ticket_read_only                                  : false
        ticket_scope_includes_open_queue                  : false
        ticket_scope_includes_actor_assigned              : false
        ticket_scope_includes_actor_requested             : false
        ticket_scope_includes_department_employee_requests: false
        task_scope                                        : "all"
        can_create_tickets                                : false
        can_create_users_globally                         : true
        can_create_users_in_department                    : false
        can_create_tasks_in_department                    : false
        can_create_tasks_globally                         : true
        can_create_technicians_or_employees_in_department : false
      }
    }
  }

  test "should return TI manager department scope and creation permissions" {
    expect.to_equal ($response) {
      value = {
        actor_id                                          : 20
        perfil_id                                         : 2
        departamento_id                                   : 1
        ticket_scope                                      : "global_read_only"
        ticket_read_only                                  : true
        ticket_scope_includes_open_queue                  : false
        ticket_scope_includes_actor_assigned              : false
        ticket_scope_includes_actor_requested             : false
        ticket_scope_includes_department_employee_requests: false
        task_scope                                        : "own_department"
        can_create_tickets                                : true
        can_create_users_globally                         : false
        can_create_users_in_department                    : true
        can_create_tasks_in_department                    : true
        can_create_tasks_globally                         : false
        can_create_technicians_or_employees_in_department : true
      }
    }
  }

  test "should return non-TI manager employee-request scope" {
    expect.to_equal ($response) {
      value = {
        actor_id                                          : 21
        perfil_id                                         : 2
        departamento_id                                   : 7
        ticket_scope                                      : "own_and_department_employee_requests_read_only"
        ticket_read_only                                  : true
        ticket_scope_includes_open_queue                  : false
        ticket_scope_includes_actor_assigned              : false
        ticket_scope_includes_actor_requested             : true
        ticket_scope_includes_department_employee_requests: true
        task_scope                                        : "own_department"
        can_create_tickets                                : true
        can_create_users_globally                         : false
        can_create_users_in_department                    : true
        can_create_tasks_in_department                    : true
        can_create_tasks_globally                         : false
        can_create_technicians_or_employees_in_department : true
      }
    }
  }

  test "should return technician queue and assigned task scopes" {
    expect.to_equal ($response) {
      value = {
        actor_id                                          : 30
        perfil_id                                         : 3
        departamento_id                                   : 7
        ticket_scope                                      : "open_queue_or_actor_assigned"
        ticket_read_only                                  : false
        ticket_scope_includes_open_queue                  : true
        ticket_scope_includes_actor_assigned              : true
        ticket_scope_includes_actor_requested             : false
        ticket_scope_includes_department_employee_requests: false
        task_scope                                        : "actor_assigned"
        can_create_tickets                                : false
        can_create_users_globally                         : false
        can_create_users_in_department                    : false
        can_create_tasks_in_department                    : false
        can_create_tasks_globally                         : false
        can_create_technicians_or_employees_in_department : false
      }
    }
  }

  test "should return employee requester-only scope" {
    expect.to_equal ($response) {
      value = {
        actor_id                                          : 40
        perfil_id                                         : 4
        departamento_id                                   : 7
        ticket_scope                                      : "actor_requested"
        ticket_read_only                                  : true
        ticket_scope_includes_open_queue                  : false
        ticket_scope_includes_actor_assigned              : false
        ticket_scope_includes_actor_requested             : true
        ticket_scope_includes_department_employee_requests: false
        task_scope                                        : "none"
        can_create_tickets                                : true
        can_create_users_globally                         : false
        can_create_users_in_department                    : false
        can_create_tasks_in_department                    : false
        can_create_tasks_globally                         : false
        can_create_technicians_or_employees_in_department : false
      }
    }
  }

  guid = "o5Atp-CxNvJALiZoNBf2tnGfiYo"
}