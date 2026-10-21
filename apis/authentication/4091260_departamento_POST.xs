// Create a departamento lookup record; only administrators may mutate lookup data.
query departamento verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Department name
    text nome? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.add departamento {
      data = {nome: $input.nome}
    } as $created_departamento
  
    var $departamento {
      value = {
        id  : $created_departamento.id
        nome: $created_departamento.nome
      }
    }
  }

  response = $departamento
}