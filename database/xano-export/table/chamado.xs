table chamado {
  auth = false

  schema {
    int id
    text titulo? filters=trim
    text descricao? filters=trim
  
    // Solução final registrada para o chamado.
    text? solucao_final?
  
    timestamp created_at?=now {
      visibility = "private"
    }
  
    int status_chamado_id? {
      table = "status_chamado"
    }
  
    int categoria_chamado_id? {
      table = "categoria_chamado"
    }
  
    int prioridade_id? {
      table = "prioridade"
    }
  
    date? atualizado_em?
    date? resolvido_em?
    int ativo_id? {
      table = "ativo"
    }
  
    int solicitante_id? {
      table = "user"
    }
  
    int? responsavel_id? {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "NMhLPBYvk-zraSVTyslfyvGyzns"
}