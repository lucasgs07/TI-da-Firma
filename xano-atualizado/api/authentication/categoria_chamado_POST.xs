// Create a categoria_chamado lookup record; only administrators may mutate lookup data.
query categoria_chamado verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Ticket category name
    text nome? filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.add categoria_chamado {
      data = {nome: $input.nome}
    } as $created_categoria_chamado
  
    var $categoria_chamado {
      value = {
        id  : $created_categoria_chamado.id
        nome: $created_categoria_chamado.nome
      }
    }
  }

  response = $categoria_chamado
  guid = "O_6FUR7Sjf7QbDQNNvhho3SANic"
}