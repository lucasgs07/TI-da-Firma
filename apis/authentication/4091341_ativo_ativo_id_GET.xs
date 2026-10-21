// Get ativo record
query "ativo/{ativo_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int ativo_id? filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "You are not authorized to access assets."
    }
  
    db.get ativo {
      field_name = "id"
      field_value = $input.ativo_id
    } as $ativo
  
    precondition ($ativo != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  }

  response = $ativo
}