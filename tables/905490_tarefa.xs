table tarefa {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text titulo? filters=trim
    text? descricao? filters=trim
  
    // Solução aplicada para concluir a tarefa.
    text? solucao_aplicada?
  
    date? prazo?
    date? concluido_em?
    int solicitante_id? {
      table = "user"
    }
  
    int responsavel_id? {
      table = "user"
    }
  
    // Authoritative membership; empty on legacy tasks, which use responsavel_id.
    int[] responsaveis_ids? {
      table = "user"
    }
  
    int chamado_id? {
      table = "chamado"
    }
  
    int prioridade_id? {
      table = "prioridade"
    }
  
    int status_chamado_id? {
      table = "status_chamado"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "KLfY3QPTfGDeRrOT2gPkDDwOnEM"
}