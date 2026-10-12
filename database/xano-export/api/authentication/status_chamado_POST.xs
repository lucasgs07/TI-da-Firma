// Create a status_chamado lookup record; only administrators may mutate lookup data.
query status_chamado verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Ticket status name
    text nome? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.add status_chamado {
      data = {nome: $input.nome}
    } as $created_status_chamado
  
    var $status_chamado {
      value = {
        id  : $created_status_chamado.id
        nome: $created_status_chamado.nome
      }
    }
  }

  response = $status_chamado
  guid = "Bzt-e4RxlGL34oTbV-iPxzLaLW4"
}