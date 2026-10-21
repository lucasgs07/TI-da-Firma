// Create a perfil lookup record; only administrators may mutate lookup data.
query perfil verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Profile name
    text name? filters=trim
  
    // Optional profile description
    text? descricao? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.add perfil {
      data = {name: $input.name, descricao: $input.descricao}
    } as $created_perfil
  
    var $perfil {
      value = {
        id       : $created_perfil.id
        name     : $created_perfil.name
        descricao: $created_perfil.descricao
      }
    }
  }

  response = $perfil
}