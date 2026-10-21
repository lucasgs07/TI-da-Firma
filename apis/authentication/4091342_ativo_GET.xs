// Query all ativo records
query ativo verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "You are not authorized to access assets."
    }
  
    db.query ativo {
      return = {type: "list"}
    } as $ativo
  }

  response = $ativo
}