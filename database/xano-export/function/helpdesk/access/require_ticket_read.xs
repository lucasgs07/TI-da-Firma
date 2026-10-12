// Authorize reading one ticket according to authenticated profile, ownership, department, and the TI manager global read-only exception.
function "helpdesk/access/require_ticket_read" {
  input {
    // ID of the ticket to check.
    int ticket_id
  }

  stack {
    function.run "helpdesk/access/get_actor_context" {
      mock = {
        "should allow administrator global ticket read"                          : {id: 10, name: "Admin", perfil_id: 1, departamento_id: 7}
        "should allow TI manager global read-only ticket access"                 : {id: 20, name: "TI Manager", perfil_id: 2, departamento_id: 1}
        "should allow non-TI manager own requester ticket"                       : {id: 21, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should allow non-TI manager same-department employee requester"         : {id: 21, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should deny non-TI manager cross-department employee requester"         : {id: 21, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should deny non-TI manager non-employee requester"                      : {id: 21, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should allow technician assigned ticket"                                : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should allow technician open unassigned queue ticket"                   : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should deny technician unassigned non-open ticket"                      : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should deny technician ticket assigned to another user"                 : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should allow technician legacy assignment without relation rows"        : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should allow technician in multi-assignee relation despite legacy owner": {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should deny legacy owner when relation excludes technician"             : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should allow employee own requester ticket"                             : {id: 40, name: "Employee", perfil_id: 4, departamento_id: 7}
        "should deny employee other requester ticket"                            : {id: 40, name: "Employee", perfil_id: 4, departamento_id: 7}
      }
    } as $actor
  
    db.get chamado {
      field_name = "id"
      field_value = $input.ticket_id
      output = ["id", "status_chamado_id", "solicitante_id", "responsavel_id"]
      mock = {
        "should allow administrator global ticket read"                          : {id: 501, status_chamado_id: null, solicitante_id: 900, responsavel_id: 901}
        "should allow TI manager global read-only ticket access"                 : {id: 502, status_chamado_id: null, solicitante_id: 900, responsavel_id: 901}
        "should allow non-TI manager own requester ticket"                       : {id: 503, status_chamado_id: null, solicitante_id: 21, responsavel_id: 901}
        "should allow non-TI manager same-department employee requester"         : {id: 504, status_chamado_id: null, solicitante_id: 904, responsavel_id: 901}
        "should deny non-TI manager cross-department employee requester"         : {id: 505, status_chamado_id: null, solicitante_id: 905, responsavel_id: 901}
        "should deny non-TI manager non-employee requester"                      : {id: 506, status_chamado_id: null, solicitante_id: 906, responsavel_id: 901}
        "should allow technician assigned ticket"                                : {id: 507, status_chamado_id: null, solicitante_id: 900, responsavel_id: 30}
        "should allow technician open unassigned queue ticket"                   : {id: 508, status_chamado_id: 1, solicitante_id: 900, responsavel_id: null}
        "should deny technician unassigned non-open ticket"                      : {id: 509, status_chamado_id: 2, solicitante_id: 900, responsavel_id: null}
        "should deny technician ticket assigned to another user"                 : {id: 510, status_chamado_id: 1, solicitante_id: 900, responsavel_id: 31}
        "should allow technician legacy assignment without relation rows"        : {id: 513, status_chamado_id: null, solicitante_id: 900, responsavel_id: 30}
        "should allow technician in multi-assignee relation despite legacy owner": {id: 514, status_chamado_id: null, solicitante_id: 900, responsavel_id: 31}
        "should deny legacy owner when relation excludes technician"             : {id: 515, status_chamado_id: null, solicitante_id: 900, responsavel_id: 30}
        "should allow employee own requester ticket"                             : {id: 511, status_chamado_id: null, solicitante_id: 40, responsavel_id: 901}
        "should deny employee other requester ticket"                            : {id: 512, status_chamado_id: null, solicitante_id: 41, responsavel_id: 901}
      }
    } as $ticket
  
    precondition ($ticket != null) {
      error_type = "accessdenied"
      error = "Ticket was not found or is not available."
    }
  
    var $can_read {
      value = false
    }
  
    var $read_only {
      value = false
    }
  
    var $scope_name {
      value = ""
    }
  
    switch ($actor.perfil_id) {
      case (1) {
        var.update $can_read {
          value = true
        }
      
        var.update $scope_name {
          value = "all"
        }
      } break
    
      case (2) {
        var.update $read_only {
          value = true
        }
      
        conditional {
          if ($actor.departamento_id == 1) {
            var.update $can_read {
              value = true
            }
          
            var.update $scope_name {
              value = "global_read_only"
            }
          }
        
          elseif ($ticket.solicitante_id == $actor.id) {
            var.update $can_read {
              value = true
            }
          
            var.update $scope_name {
              value = "own_ticket_read_only"
            }
          }
        
          else {
            conditional {
              if ($ticket.solicitante_id != null) {
                db.get user {
                  field_name = "id"
                  field_value = $ticket.solicitante_id
                  output = ["id", "perfil_id", "departamento_id"]
                  mock = {
                    "should allow non-TI manager same-department employee requester": {id: 904, perfil_id: 4, departamento_id: 7}
                    "should deny non-TI manager cross-department employee requester": {id: 905, perfil_id: 4, departamento_id: 8}
                    "should deny non-TI manager non-employee requester"             : {id: 906, perfil_id: 3, departamento_id: 7}
                  }
                } as $requester
              
                conditional {
                  if ($requester != null && $requester.perfil_id == 4 && $requester.departamento_id == $actor.departamento_id) {
                    var.update $can_read {
                      value = true
                    }
                  
                    var.update $scope_name {
                      value = "department_employee_ticket_read_only"
                    }
                  }
                }
              }
            }
          }
        }
      } break
    
      case (3) {
        // Load ticket assignment relations; these are authoritative when present.
        db.query chamado_tecnico {
          where = $db.chamado_tecnico.chamado_id == $ticket.id
          return = {type: "list"}
          mock = {
            "should allow technician assigned ticket"                                : [{id: 1, chamado_id: 507, tecnico_id: 30}]
            "should allow technician open unassigned queue ticket"                   : []
            "should deny technician unassigned non-open ticket"                      : []
            "should deny technician ticket assigned to another user"                 : [{id: 2, chamado_id: 510, tecnico_id: 31}]
            "should allow technician legacy assignment without relation rows"        : []
            "should allow technician in multi-assignee relation despite legacy owner": ```
              [
                {id: 3, chamado_id: 514, tecnico_id: 31},
                {id: 4, chamado_id: 514, tecnico_id: 30}
              ]
              ```
            "should deny legacy owner when relation excludes technician"             : [{id: 5, chamado_id: 515, tecnico_id: 31}]
          }
        } as $ticket_technician_assignments
      
        // Determine whether relation assignments exist before considering the legacy owner field.
        var $assignment_count {
          value = $ticket_technician_assignments|count
        }
      
        // Check whether this technician belongs to the ticket's assignment relation.
        db.query chamado_tecnico {
          where = $db.chamado_tecnico.chamado_id == $ticket.id && $db.chamado_tecnico.tecnico_id == $actor.id
          return = {type: "single"}
          mock = {
            "should allow technician assigned ticket"                                : {id: 1, chamado_id: 507, tecnico_id: 30}
            "should allow technician open unassigned queue ticket"                   : null
            "should deny technician unassigned non-open ticket"                      : null
            "should deny technician ticket assigned to another user"                 : null
            "should allow technician legacy assignment without relation rows"        : null
            "should allow technician in multi-assignee relation despite legacy owner": {id: 4, chamado_id: 514, tecnico_id: 30}
            "should deny legacy owner when relation excludes technician"             : null
          }
        } as $actor_ticket_assignment
      
        var $actor_is_assigned {
          value = ($actor_ticket_assignment != null)
        }
      
        conditional {
          if ($assignment_count > 0) {
            conditional {
              if ($actor_is_assigned) {
                var.update $can_read {
                  value = true
                }
              
                var.update $scope_name {
                  value = "actor_assigned"
                }
              }
            }
          }
        
          elseif ($ticket.responsavel_id == $actor.id) {
            var.update $can_read {
              value = true
            }
          
            var.update $scope_name {
              value = "actor_assigned"
            }
          }
        
          else {
            conditional {
              if ($assignment_count == 0 && $ticket.responsavel_id == null && $ticket.status_chamado_id != null) {
                db.get status_chamado {
                  field_name = "id"
                  field_value = $ticket.status_chamado_id
                  output = ["id", "nome"]
                  mock = {
                    "should allow technician open unassigned queue ticket": {id: 1, nome: "Aberto"}
                    "should deny technician unassigned non-open ticket"   : {id: 2, nome: "Em andamento"}
                  }
                } as $ticket_status
              
                conditional {
                  if ($ticket_status != null && $ticket_status.nome == "Aberto") {
                    var.update $can_read {
                      value = true
                    }
                  
                    var.update $scope_name {
                      value = "open_queue"
                    }
                  }
                }
              }
            }
          }
        }
      } break
    
      case (4) {
        var.update $read_only {
          value = true
        }
      
        conditional {
          if ($ticket.solicitante_id == $actor.id) {
            var.update $can_read {
              value = true
            }
          
            var.update $scope_name {
              value = "actor_requested"
            }
          }
        }
      } break
    }
  
    precondition ($can_read) {
      error_type = "accessdenied"
      error = "Ticket was not found or is not available."
    }
  
    var $authorization {
      value = {
        ticket_id: $ticket.id
        actor_id : $actor.id
        scope    : $scope_name
        read_only: $read_only
      }
    }
  }

  response = $authorization

  test "should allow administrator global ticket read" {
    input = {ticket_id: 501}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 501
        actor_id : 10
        scope    : "all"
        read_only: false
      }
    }
  }

  test "should allow TI manager global read-only ticket access" {
    input = {ticket_id: 502}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 502
        actor_id : 20
        scope    : "global_read_only"
        read_only: true
      }
    }
  }

  test "should allow non-TI manager own requester ticket" {
    input = {ticket_id: 503}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 503
        actor_id : 21
        scope    : "own_ticket_read_only"
        read_only: true
      }
    }
  }

  test "should allow non-TI manager same-department employee requester" {
    input = {ticket_id: 504}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 504
        actor_id : 21
        scope    : "department_employee_ticket_read_only"
        read_only: true
      }
    }
  }

  test "should deny non-TI manager cross-department employee requester" {
    input = {ticket_id: 505}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should deny non-TI manager non-employee requester" {
    input = {ticket_id: 506}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should allow technician assigned ticket" {
    input = {ticket_id: 507}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 507
        actor_id : 30
        scope    : "actor_assigned"
        read_only: false
      }
    }
  }

  test "should allow technician open unassigned queue ticket" {
    input = {ticket_id: 508}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 508
        actor_id : 30
        scope    : "open_queue"
        read_only: false
      }
    }
  }

  test "should deny technician unassigned non-open ticket" {
    input = {ticket_id: 509}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should deny technician ticket assigned to another user" {
    input = {ticket_id: 510}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should allow technician legacy assignment without relation rows" {
    input = {ticket_id: 513}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 513
        actor_id : 30
        scope    : "actor_assigned"
        read_only: false
      }
    }
  }

  test "should allow technician in multi-assignee relation despite legacy owner" {
    input = {ticket_id: 514}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 514
        actor_id : 30
        scope    : "actor_assigned"
        read_only: false
      }
    }
  }

  test "should deny legacy owner when relation excludes technician" {
    input = {ticket_id: 515}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should allow employee own requester ticket" {
    input = {ticket_id: 511}
  
    expect.to_equal ($response) {
      value = {
        ticket_id: 511
        actor_id : 40
        scope    : "actor_requested"
        read_only: true
      }
    }
  }

  test "should deny employee other requester ticket" {
    input = {ticket_id: 512}
  
    expect.to_throw {
      exception = ""
    }
  }

  guid = "UvfAYEeiK2Fqx3Umub6c4zbBhFo"
}