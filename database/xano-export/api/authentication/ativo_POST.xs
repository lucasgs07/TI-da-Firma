// Add ativo record
query ativo verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text nome? filters=trim
    text patrimonio? filters=trim
    text modelo? filters=trim
    text marca? filters=trim
    text numero_serie? filters=trim
    date data_aquisicao?
    int status_ativo_id?
    int departamento_id?
    int user_id?
    int tipo_ativo_id?
  }

  stack {
    function.run "helpdesk/access/require_admin" as $actor
    var $payload {
      value = {}
    }
  
    conditional {
      if ($input.nome != null) {
        var.update $payload {
          value = $payload|set:"nome":$input.nome
        }
      }
    }
  
    conditional {
      if ($input.patrimonio != null) {
        var.update $payload {
          value = $payload
            |set:"patrimonio":$input.patrimonio
        }
      }
    }
  
    conditional {
      if ($input.modelo != null) {
        var.update $payload {
          value = $payload|set:"modelo":$input.modelo
        }
      }
    }
  
    conditional {
      if ($input.marca != null) {
        var.update $payload {
          value = $payload|set:"marca":$input.marca
        }
      }
    }
  
    conditional {
      if ($input.numero_serie != null) {
        var.update $payload {
          value = $payload
            |set:"numero_serie":$input.numero_serie
        }
      }
    }
  
    conditional {
      if ($input.data_aquisicao != null) {
        var.update $payload {
          value = $payload
            |set:"data_aquisicao":$input.data_aquisicao
        }
      }
    }
  
    conditional {
      if ($input.status_ativo_id != null) {
        var.update $payload {
          value = $payload
            |set:"status_ativo_id":$input.status_ativo_id
        }
      }
    }
  
    conditional {
      if ($input.departamento_id != null) {
        var.update $payload {
          value = $payload
            |set:"departamento_id":$input.departamento_id
        }
      }
    }
  
    conditional {
      if ($input.user_id != null) {
        var.update $payload {
          value = $payload|set:"user_id":$input.user_id
        }
      }
    }
  
    conditional {
      if ($input.tipo_ativo_id != null) {
        var.update $payload {
          value = $payload
            |set:"tipo_ativo_id":$input.tipo_ativo_id
        }
      }
    }
  
    db.add ativo {
      data = {
        nome           : $input.nome
        patrimonio     : $input.patrimonio
        modelo         : $input.modelo
        marca          : $input.marca
        numero_serie   : $input.numero_serie
        data_aquisicao : $input.data_aquisicao
        status_ativo_id: $input.status_ativo_id
        departamento_id: $input.departamento_id
        user_id        : $input.user_id
        tipo_ativo_id  : $input.tipo_ativo_id
      }
    } as $ativo
  }

  response = $ativo
  guid = "iAC0rbkU1M58OdEoAtGWmVWJuyM"
}