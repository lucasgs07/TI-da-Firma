// Global ticket counts; assignments never multiply a ticket.
query "helpdesk/metrics/tickets" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/require_admin" {
      mock = {
        "all status groups": {id: 10, perfil_id: 1}
        "empty dashboard"  : {id: 10, perfil_id: 1}
      }
    } as $admin
  
    db.query chamado {
      join = {
        status: {
          table: "status_chamado"
          type : "left"
          where: $db.chamado.status_chamado_id == $db.status.id
        }
      }
    
      eval = {status_name: $db.status.nome}
      return = {type: "list"}
      output = ["id", "status_name"]
      mock = {
        "all status groups": ```
          [
            {id: 1, status_name: "Aberto"}
            {id: 2, status_name: "Em Análise"}
            {id: 3, status_name: "Em atendimento"}
            {id: 4, status_name: "Aguardando usuário"}
            {id: 5, status_name: "Resolvido"}
            {id: 6, status_name: "Fechado"}
            {id: 7, status_name: null}
            {id: 8, status_name: "Outro"}
          ]
          ```
        "empty dashboard"  : []
      }
    } as $tickets
  
    var $abertos {
      value = 0
    }
  
    var $em_andamento {
      value = 0
    }
  
    var $finalizados {
      value = 0
    }
  
    var $nao_classificados {
      value = 0
    }
  
    foreach ($tickets) {
      each as $ticket {
        conditional {
          if ($ticket.status_name == "Aberto") {
            var.update $abertos {
              value = $abertos + 1
            }
          }
        
          elseif ($ticket.status_name == "Em Análise" || $ticket.status_name == "Em atendimento" || $ticket.status_name == "Aguardando usuário") {
            var.update $em_andamento {
              value = $em_andamento + 1
            }
          }
        
          elseif ($ticket.status_name == "Resolvido" || $ticket.status_name == "Fechado") {
            var.update $finalizados {
              value = $finalizados + 1
            }
          }
        
          else {
            var.update $nao_classificados {
              value = $nao_classificados + 1
            }
          }
        }
      }
    }
  
    var $metrics {
      value = {
        abertos          : $abertos
        em_andamento     : $em_andamento
        finalizados      : $finalizados
        nao_classificados: $nao_classificados
        total            : $tickets|count
      }
    }
  }

  response = $metrics

  test "all status groups" {
    expect.to_equal ($response) {
      value = {
        abertos          : 1
        em_andamento     : 3
        finalizados      : 2
        nao_classificados: 2
        total            : 8
      }
    }
  }

  test "empty dashboard" {
    expect.to_equal ($response) {
      value = {
        abertos          : 0
        em_andamento     : 0
        finalizados      : 0
        nao_classificados: 0
        total            : 0
      }
    }
  }

  guid = "JVwPj_BR5cdjyvZanjvoOeU37X0"
}