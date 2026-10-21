table ativo {
  auth = false

  schema {
    int id
    text nome? filters=trim
    text patrimonio? filters=trim
    text modelo? filters=trim
    text marca? filters=trim
    text numero_serie? filters=trim
    date? data_aquisicao?
    int status_ativo_id? {
      table = "status_ativo"
    }
  
    int departamento_id? {
      table = "departamento"
    }
  
    int user_id? {
      table = "user"
    }
  
    int tipo_ativo_id? {
      table = "tipo_ativo"
    }
  }

  index = [{type: "primary", field: [{name: "id"}]}]
}