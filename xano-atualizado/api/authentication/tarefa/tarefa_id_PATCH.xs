// Managers may reassign within their department; technicians may complete their own task.
// Allow department managers to reassign a task to an in-department technician and assigned technicians to complete their own task.
query "tarefa/{tarefa_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    // Task ID from the route.
    int tarefa_id filters=min:1
  
    // Replacement technician; managers may reassign only within their department.
    int responsavel_id?
  
    // Non-empty applied solution required for technician completion.
    text solucao_aplicada? filters=trim
  
    // Technician completion action; the only accepted value is 'Concluída'.
    text status_nome? filters=trim
  
    // Reserved for rejection; task assignment is server-managed.
    int responsible_id?
  
    // Reserved for rejection; requester identity is server-managed.
    int solicitante_id?
  
    // Reserved for rejection; requester identity is server-managed.
    int requester_id?
  
    // Reserved for rejection; status IDs are server-managed.
    int status_chamado_id?
  
    // Reserved for rejection; status IDs are server-managed.
    int status_id?
  
    // Reserved for rejection; task title is not editable through this endpoint.
    text titulo?
  
    // Reserved for rejection; task description is not editable through this endpoint.
    text descricao?
  
    // Reserved for rejection; linked ticket is not editable through this endpoint.
    int chamado_id?
  
    // Reserved for rejection; task priority is not editable through this endpoint.
    int prioridade_id?
  }

  stack {
    util.get_all_input as $provided_input
    function.run "helpdesk/access/get_actor_context" as $actor
    var $requested_responsavel_id {
      value = null
    }
  
    var $requested_solution {
      value = null
    }
  
    var $requested_status {
      value = null
    }
  
    conditional {
      if ($provided_input.responsavel_id > 0) {
        var.update $requested_responsavel_id {
          value = $provided_input.responsavel_id
        }
      }
    }
  
    conditional {
      if ($provided_input|has:"solucao_aplicada") {
        var.update $requested_solution {
          value = $provided_input.solucao_aplicada
        }
      }
    }
  
    conditional {
      if ($provided_input|has:"status_nome") {
        var.update $requested_status {
          value = $provided_input.status_nome
        }
      }
    }
  
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "Only administrators, managers and technicians may update tasks."
    }
  
    conditional {
      if ($provided_input|has:"responsible_id" || $provided_input|has:"solicitante_id" || $provided_input|has:"requester_id" || $provided_input|has:"status_chamado_id" || $provided_input|has:"status_id" || $provided_input|has:"titulo" || $provided_input|has:"descricao" || $provided_input|has:"chamado_id" || $provided_input|has:"prioridade_id") {
        precondition (false) {
          error_type = "inputerror"
          error = "Only an authorized technician reassignment or task completion is allowed; other task fields are server-managed or immutable."
        }
      }
    }
  
    db.get tarefa {
      field_name = "id"
      field_value = $input.tarefa_id
      output = [
        "id"
        "titulo"
        "descricao"
        "solucao_aplicada"
        "prazo"
        "concluido_em"
        "solicitante_id"
        "responsavel_id"
        "chamado_id"
        "prioridade_id"
        "status_chamado_id"
      ]
    } as $tarefa
  
    precondition ($tarefa != null) {
      error_type = "notfound"
      error = "Task not found."
    }
  
    conditional {
      if ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
        precondition ($requested_responsavel_id != null && $requested_solution == null && $requested_status == null) {
          error_type = "inputerror"
          error = "Managers may only reassign a task by providing a technician ID."
        }
      
        db.get user {
          field_name = "id"
          field_value = $tarefa.responsavel_id
          output = ["id", "perfil_id", "departamento_id"]
        } as $current_responsavel
      
        precondition ($current_responsavel != null && ($actor.perfil_id == 1 || ($current_responsavel.perfil_id == 3 && $current_responsavel.departamento_id == $actor.departamento_id))) {
          error_type = "accessdenied"
          error = "Managers may reassign only tasks currently assigned to technicians in their department."
        }
      
        function.run "helpdesk/access/authorize_target_user" {
          input = {
            target_user_id    : $requested_responsavel_id
            expected_perfil_id: 3
          }
        } as $new_responsavel
      
        db.patch tarefa {
          field_name = "id"
          field_value = $input.tarefa_id
          data = {responsavel_id: $new_responsavel.id}
        } as $patched_tarefa
      }
    
      else {
        precondition ($tarefa.responsavel_id == $actor.id) {
          error_type = "accessdenied"
          error = "Only the assigned technician may complete this task."
        }
      
        precondition ($requested_responsavel_id == null) {
          error_type = "accessdenied"
          error = "Technicians may not reassign tasks."
        }
      
        precondition ($requested_status == "Concluída") {
          error_type = "inputerror"
          error = "Technicians may only complete a task by requesting the exact status name 'Concluída'."
        }
      
        precondition ($requested_solution != null && ($requested_solution|strlen) > 0) {
          error_type = "inputerror"
          error = "A non-empty applied solution is required to complete a task."
        }
      
        db.query status_chamado {
          where = $db.status_chamado.nome == "Concluída"
          return = {type: "single"}
        } as $completion_status
      
        precondition ($completion_status != null) {
          error = "Task completion is not configured: status_chamado has no exact 'Concluída' row."
        }
      
        var $current_status {
          value = null
        }
      
        conditional {
          if ($tarefa.status_chamado_id != null) {
            db.get status_chamado {
              field_name = "id"
              field_value = $tarefa.status_chamado_id
              output = ["id", "nome"]
            } as $loaded_current_status
          
            var.update $current_status {
              value = $loaded_current_status
            }
          
            precondition ($current_status != null) {
              error = "The task status could not be verified; no task changes were made."
            }
          }
        }
      
        var $is_completed {
          value = false
        }
      
        conditional {
          if ($current_status != null && $current_status.nome == "Concluída") {
            precondition ($current_status.id == $completion_status.id) {
              error = "The task's completion status does not match the configured 'Concluída' status."
            }
          
            var.update $is_completed {
              value = true
            }
          }
        }
      
        conditional {
          if ($is_completed) {
            precondition ($tarefa.concluido_em != null) {
              error = "The completed task is missing its server-generated completion date."
            }
          
            precondition ($requested_solution == $tarefa.solucao_aplicada) {
              error_type = "accessdenied"
              error = "Completed tasks are immutable; only an identical solution may be submitted for idempotent completion."
            }
          }
        
          else {
            precondition ($tarefa.concluido_em == null) {
              error = "The task has completion data but is not in the configured completion status."
            }
          
            db.patch tarefa {
              field_name = "id"
              field_value = $input.tarefa_id
              data = {
                solucao_aplicada : $requested_solution
                status_chamado_id: $completion_status.id
                concluido_em     : "now"|format_timestamp:"Y-m-d"
              }
            } as $patched_tarefa
          }
        }
      }
    }
  
    db.get tarefa {
      field_name = "id"
      field_value = $input.tarefa_id
      output = [
        "id"
        "titulo"
        "descricao"
        "solucao_aplicada"
        "prazo"
        "concluido_em"
        "solicitante_id"
        "responsavel_id"
        "chamado_id"
        "prioridade_id"
        "status_chamado_id"
      ]
    } as $final_tarefa
  
    var $final_status_name {
      value = null
    }
  
    conditional {
      if ($final_tarefa.status_chamado_id != null) {
        db.get status_chamado {
          field_name = "id"
          field_value = $final_tarefa.status_chamado_id
          output = ["id", "nome"]
        } as $final_status
      
        precondition ($final_status != null) {
          error = "The saved task status could not be verified."
        }
      
        var.update $final_status_name {
          value = $final_status.nome
        }
      }
    }
  
    // Return only explicitly whitelisted task fields and the related status name.
    var $public_task {
      value = {
        id               : $final_tarefa.id
        titulo           : $final_tarefa.titulo
        descricao        : $final_tarefa.descricao
        solucao_aplicada : $final_tarefa.solucao_aplicada
        prazo            : $final_tarefa.prazo
        concluido_em     : $final_tarefa.concluido_em
        solicitante_id   : $final_tarefa.solicitante_id
        responsavel_id   : $final_tarefa.responsavel_id
        chamado_id       : $final_tarefa.chamado_id
        prioridade_id    : $final_tarefa.prioridade_id
        status_chamado_id: $final_tarefa.status_chamado_id
        status_nome      : $final_status_name
      }
    }
  }

  response = $public_task
  guid = "UrTo-xuweQqFYbtfR8YVeoNTsKc"
}