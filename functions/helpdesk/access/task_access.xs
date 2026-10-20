// Resolve task membership and access consistently, including legacy single-owner tasks.
function "helpdesk/access/task_access" {
  input {
    int tarefa_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" {
      mock = {
        "secondary technician can read"           : {id: 30, perfil_id: 3, departamento_id: 1}
        "legacy responsible can read"             : {id: 30, perfil_id: 3, departamento_id: 1}
        "secondary employee can read"             : {id: 40, perfil_id: 4, departamento_id: 7}
        "unassigned employee cannot read"         : {id: 40, perfil_id: 4, departamento_id: 7}
        "manager cannot manage outside department": {id: 20, perfil_id: 2, departamento_id: 1}
      }
    } as $actor
  
    db.get tarefa {
      field_name = "id"
      field_value = $input.tarefa_id
      mock = {
        "secondary technician can read"           : {id: 10, responsavel_id: 31, responsaveis_ids: [31, 30]}
        "legacy responsible can read"             : {id: 10, responsavel_id: 30, responsaveis_ids: []}
        "secondary employee can read"             : {id: 10, responsavel_id: 41, responsaveis_ids: [41, 40]}
        "unassigned employee cannot read"         : {id: 10, responsavel_id: 40, responsaveis_ids: [30, 31]}
        "manager cannot manage outside department": {id: 10, responsavel_id: 31, responsaveis_ids: [31, 40]}
      }
    } as $task
  
    precondition ($task != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    var $ids {
      value = []
    }
  
    conditional {
      if ($task.responsaveis_ids != null && ($task.responsaveis_ids|count) > 0) {
        var.update $ids {
          value = $task.responsaveis_ids
        }
      }
    
      elseif ($task.responsavel_id != null && $task.responsavel_id > 0) {
        array.push $ids {
          value = $task.responsavel_id
        }
      }
    }
  
    array.has ($ids) if ($this == $actor.id) as $assigned
    var $department_scope {
      value = (($ids|count) > 0 && $actor.departamento_id != null)
    }
  
    var $people {
      value = []
    }
  
    foreach ($ids) {
      each as $member_id {
        db.get user {
          field_name = "id"
          field_value = $member_id
          output = ["id", "name", "perfil_id", "departamento_id"]
          mock = {
            "secondary technician can read"           : {id: 31, name: "Technician", perfil_id: 3, departamento_id: 1}
            "legacy responsible can read"             : {id: 30, name: "Legacy", perfil_id: 3, departamento_id: 1}
            "secondary employee can read"             : {id: 41, name: "Employee", perfil_id: 4, departamento_id: 7}
            "unassigned employee cannot read"         : {id: 31, name: "Technician", perfil_id: 3, departamento_id: 1}
            "manager cannot manage outside department": {id: 40, name: "External employee", perfil_id: 4, departamento_id: 7}
          }
        } as $member
      
        conditional {
          if ($member == null) {
            var.update $department_scope {
              value = false
            }
          
            array.push $people {
              value = {id: $member_id, name: "Unavailable user"}
            }
          }
        
          else {
            array.push $people {
              value = {id: $member.id, name: $member.name}
            }
          
            conditional {
              if ($member.departamento_id != $actor.departamento_id || ($actor.departamento_id == 1 && $member.perfil_id != 3) || ($actor.departamento_id != 1 && $member.perfil_id != 4)) {
                var.update $department_scope {
                  value = false
                }
              }
            }
          }
        }
      }
    }
  
    var $can_manage {
      value = ($actor.perfil_id == 1 || ($actor.perfil_id == 2 && $department_scope))
    }
  
    var $can_read {
      value = ($can_manage || (($actor.perfil_id == 3 || $actor.perfil_id == 4) && $assigned))
    }
  
    var $public_task {
      value = {
        id               : $task.id
        titulo           : $task.titulo
        descricao        : $task.descricao
        solucao_aplicada : $task.solucao_aplicada
        prazo            : $task.prazo
        concluido_em     : $task.concluido_em
        solicitante_id   : $task.solicitante_id
        responsavel_id   : $task.responsavel_id
        responsaveis_ids : $ids
        responsaveis     : $people
        chamado_id       : $task.chamado_id
        prioridade_id    : $task.prioridade_id
        status_chamado_id: $task.status_chamado_id
      }
    }
  
    var $access {
      value = {
        task      : $public_task
        assigned  : $assigned
        can_read  : $can_read
        can_manage: $can_manage
      }
    }
  }

  response = $access

  test "secondary technician can read" {
    input = {tarefa_id: 10}
  
    expect.to_equal ($response.assigned) {
      value = true
    }
  
    expect.to_equal ($response.can_read) {
      value = true
    }
  }

  test "legacy responsible can read" {
    input = {tarefa_id: 10}
  
    expect.to_equal ($response.assigned) {
      value = true
    }
  
    expect.to_equal ($response.can_read) {
      value = true
    }
  }

  test "secondary employee can read" {
    input = {tarefa_id: 10}
  
    expect.to_equal ($response.assigned) {
      value = true
    }
  
    expect.to_equal ($response.can_read) {
      value = true
    }
  }

  test "unassigned employee cannot read" {
    input = {tarefa_id: 10}
  
    expect.to_equal ($response.assigned) {
      value = false
    }
  
    expect.to_equal ($response.can_read) {
      value = false
    }
  }

  test "manager cannot manage outside department" {
    input = {tarefa_id: 10}
  
    expect.to_equal ($response.can_manage) {
      value = false
    }
  
    expect.to_equal ($response.can_read) {
      value = false
    }
  }

  guid = "Wm3yWrFzpK-d2t3MAD2_YemFc2o"
}