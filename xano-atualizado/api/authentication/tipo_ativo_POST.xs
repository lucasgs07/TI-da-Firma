// Create a tipo_ativo lookup record; only administrators may mutate lookup data.
query tipo_ativo verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Asset type name
    text nome? filters=trim
  
    // Optional asset type description
    text? descricao? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.add tipo_ativo {
      data = {nome: $input.nome, descricao: $input.descricao}
    } as $created_tipo_ativo
  
    var $tipo_ativo {
      value = {
        id       : $created_tipo_ativo.id
        nome     : $created_tipo_ativo.nome
        descricao: $created_tipo_ativo.descricao
      }
    }
  }

  response = $tipo_ativo
  guid = "n0kgkyksrMyy9UDKX3_4Q6AF_6o"
}