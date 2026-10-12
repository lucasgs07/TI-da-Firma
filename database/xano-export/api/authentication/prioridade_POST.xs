// Create a prioridade lookup record; only administrators may mutate lookup data.
query prioridade verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // Priority name
    text nome? filters=trim
  
    // Optional priority level
    int nivel?
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.add prioridade {
      data = {nome: $input.nome, nivel: $input.nivel}
    } as $created_prioridade
  
    var $prioridade {
      value = {
        id   : $created_prioridade.id
        nome : $created_prioridade.nome
        nivel: $created_prioridade.nivel
      }
    }
  }

  response = $prioridade
  guid = "Gx68Uat70Taq6G7hiO3XWSxfj6c"
}