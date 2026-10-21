// Create a status_ativo lookup record; only administrators may mutate lookup data.
query status_ativo verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Asset status name
    text nome? filters=trim
  
    // Optional asset status description
    text? descricao? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.add status_ativo {
      data = {nome: $input.nome, descricao: $input.descricao}
    } as $created_status_ativo
  
    var $status_ativo {
      value = {
        id       : $created_status_ativo.id
        nome     : $created_status_ativo.nome
        descricao: $created_status_ativo.descricao
      }
    }
  }

  response = $status_ativo
}