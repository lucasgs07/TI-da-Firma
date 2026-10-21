// Create a ticket for an authenticated employee or manager.
// Create a ticket with requester identity and initial status derived by the server.
query chamado verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Existing ticket category.
    int categoria_chamado_id filters=min:1
  
    // Existing ticket priority.
    int prioridade_id filters=min:1
  
    // Short ticket title.
    text titulo filters=trim|min:1|max:200
  
    // Details of the issue.
    text descricao filters=trim|min:1|max:10000
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 2 || $actor.perfil_id == 4) {
      error_type = "accessdenied"
      error = "Only employees and managers may create tickets."
    }
  
    db.get categoria_chamado {
      field_name = "id"
      field_value = $input.categoria_chamado_id
      output = ["id", "nome"]
    } as $category
  
    precondition ($category != null) {
      error_type = "inputerror"
      error = "The selected ticket category does not exist."
    }
  
    db.get prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
      output = ["id", "nome"]
    } as $priority
  
    precondition ($priority != null) {
      error_type = "inputerror"
      error = "The selected priority does not exist."
    }
  
    db.get status_chamado {
      field_name = "nome"
      field_value = "Aberto"
      output = ["id", "nome"]
    } as $open_status
  
    precondition ($open_status != null) {
      error = "The configured open ticket status could not be found."
    }
  
    db.add chamado {
      data = {
        titulo              : $input.titulo
        descricao           : $input.descricao
        status_chamado_id   : $open_status.id
        categoria_chamado_id: $category.id
        prioridade_id       : $priority.id
        solicitante_id      : $actor.id
        responsavel_id      : null
        atualizado_em       : now
      }
    } as $created_ticket
  
    // Return only ticket fields intended for the API consumer.
    var $public_ticket {
      value = {
        id                  : $created_ticket.id
        titulo              : $created_ticket.titulo
        descricao           : $created_ticket.descricao
        solucao_final       : $created_ticket.solucao_final
        status_chamado_id   : $open_status.id
        status_nome         : $open_status.nome
        categoria_chamado_id: $category.id
        categoria_nome      : $category.nome
        prioridade_id       : $priority.id
        prioridade_nome     : $priority.nome
        solicitante_id      : $actor.id
        solicitante_nome    : $actor.name
        responsavel_id      : null
        responsavel_nome    : null
        atualizado_em       : $created_ticket.atualizado_em
        resolvido_em        : $created_ticket.resolvido_em
      }
    }
  }

  response = $public_ticket
}