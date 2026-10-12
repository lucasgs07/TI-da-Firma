table interacao_chamado {
  auth = false

  schema {
    int id
    timestamp created_at?=now {
      visibility = "private"
    }
  
    text? mensagem? filters=trim
    int chamado_id? {
      table = "chamado"
    }
  
    int user_id? {
      table = "user"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {type: "btree", field: [{name: "created_at", op: "desc"}]}
  ]

  guid = "VcL0YTr6MSfJVXeQZ69fxNjHl-4"
}