// Return assigned ticket and task workload metrics for technicians visible to the authenticated administrator or department manager.
query "helpdesk/metrics/technicians" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Only administrators and managers may access technician workload metrics."
    }
  
    db.get status_chamado {
      field_name = "nome"
      field_value = "Aberto"
      output = ["id"]
    } as $status_aberto
  
    precondition ($status_aberto != null) {
      error = "Required status 'Aberto' could not be found."
    }
  
    db.get status_chamado {
      field_name = "nome"
      field_value = "Em Análise"
      output = ["id"]
    } as $status_em_analise
  
    precondition ($status_em_analise != null) {
      error = "Required status 'Em Análise' could not be found."
    }
  
    db.get status_chamado {
      field_name = "nome"
      field_value = "Em atendimento"
      output = ["id"]
    } as $status_em_atendimento
  
    precondition ($status_em_atendimento != null) {
      error = "Required status 'Em atendimento' could not be found."
    }
  
    db.get status_chamado {
      field_name = "nome"
      field_value = "Aguardando usuário"
      output = ["id"]
    } as $status_aguardando_usuario
  
    precondition ($status_aguardando_usuario != null) {
      error = "Required status 'Aguardando usuário' could not be found."
    }
  
    conditional {
      if ($actor.perfil_id == 1) {
        // Select all technicians for the administrator.
        db.query user {
          where = $db.user.perfil_id == 3
          return = {type: "list"}
          output = ["id", "name", "departamento_id"]
        } as $technicians
      }
    
      else {
        // Select only technicians in the manager's server-verified department.
        db.query user {
          where = $db.user.perfil_id == 3 && $db.user.departamento_id == $actor.departamento_id
          return = {type: "list"}
          output = ["id", "name", "departamento_id"]
        } as $technicians
      }
    }
  
    var $workload_rows {
      value = []
    }
  
    foreach ($technicians) {
      each as $technician {
        var $assigned_ticket_ids {
          value = []
        }
      
        var $pending_ticket_ids {
          value = []
        }
      
        // Fetch every ticket relation for this technician; the unique pair index prevents duplicate memberships.
        db.query chamado_tecnico {
          where = $db.chamado_tecnico.tecnico_id == $technician.id
          return = {type: "list"}
          output = ["chamado_id"]
        } as $technician_ticket_assignments
      
        foreach ($technician_ticket_assignments) {
          each as $ticket_assignment {
            array.push $assigned_ticket_ids {
              value = $ticket_assignment.chamado_id
            }
          }
        }
      
        // Fetch relation-assigned tickets in pending statuses.
        db.query chamado_tecnico {
          join = {
            ticket: {
              table: "chamado"
              where: $db.chamado_tecnico.chamado_id == $db.ticket.id
            }
          }
        
          where = $db.chamado_tecnico.tecnico_id == $technician.id && ($db.ticket.status_chamado_id == $status_em_analise.id || $db.ticket.status_chamado_id == $status_em_atendimento.id || $db.ticket.status_chamado_id == $status_aguardando_usuario.id)
          return = {type: "list"}
          output = ["chamado_id"]
        } as $technician_pending_assignments
      
        foreach ($technician_pending_assignments) {
          each as $pending_assignment {
            array.push $pending_ticket_ids {
              value = $pending_assignment.chamado_id
            }
          }
        }
      
        // Fetch legacy responsible tickets so assignments absent from chamado_tecnico remain represented.
        db.query chamado {
          where = $db.chamado.responsavel_id == $technician.id
          return = {type: "list"}
          output = ["id", "status_chamado_id"]
        } as $legacy_responsible_tickets
      
        foreach ($legacy_responsible_tickets) {
          each as $legacy_ticket {
            db.query chamado_tecnico {
              where = $db.chamado_tecnico.chamado_id == $legacy_ticket.id && $db.chamado_tecnico.tecnico_id == $technician.id
              return = {type: "count"}
            } as $legacy_membership_count
          
            conditional {
              if ($legacy_membership_count == 0) {
                array.push $assigned_ticket_ids {
                  value = $legacy_ticket.id
                }
              
                conditional {
                  if ($legacy_ticket.status_chamado_id == $status_em_analise.id || $legacy_ticket.status_chamado_id == $status_em_atendimento.id || $legacy_ticket.status_chamado_id == $status_aguardando_usuario.id) {
                    array.push $pending_ticket_ids {
                      value = $legacy_ticket.id
                    }
                  }
                }
              }
            }
          }
        }
      
        var $assigned_ticket_count {
          value = $assigned_ticket_ids|count
        }
      
        var $pending_ticket_count {
          value = $pending_ticket_ids|count
        }
      
        db.query tarefa {
          where = $db.tarefa.responsavel_id == $technician.id
          return = {type: "count"}
        } as $assigned_tasks
      
        db.query tarefa {
          where = $db.tarefa.responsavel_id == $technician.id && ($db.tarefa.status_chamado_id == $status_aberto.id || $db.tarefa.status_chamado_id == $status_em_analise.id || $db.tarefa.status_chamado_id == $status_em_atendimento.id || $db.tarefa.status_chamado_id == $status_aguardando_usuario.id)
          return = {type: "count"}
        } as $pending_tasks
      
        array.push $workload_rows {
          value = {
            technician_id   : $technician.id
            technician_name : $technician.name
            departamento_id : $technician.departamento_id
            tickets_assigned: $assigned_ticket_count
            tickets_pending : $pending_ticket_count
            tasks_assigned  : $assigned_tasks
            tasks_pending   : $pending_tasks
          }
        }
      }
    }
  }

  response = $workload_rows
  history = false
}