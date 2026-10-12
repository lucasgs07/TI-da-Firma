table chamado_tecnico {
  auth = false

  schema {
    int id
  
    // Chamado associado ao técnico.
    int chamado_id {
      table = "chamado"
    }
  
    // Técnico associado ao chamado.
    int tecnico_id {
      table = "user"
    }
  
    // Data e hora em que a associação foi criada.
    timestamp created_at?=now {
      visibility = "private"
    }
  }

  index = [
    {type: "primary", field: [{name: "id"}]}
    {
      type : "btree|unique"
      field: [
        {name: "chamado_id", op: "asc"}
        {name: "tecnico_id", op: "asc"}
      ]
    }
    {type: "btree", field: [{name: "tecnico_id", op: "asc"}]}
  ]

  guid = "hINbQI_8EKAlpwhv3HxjSeJIh1g"
}