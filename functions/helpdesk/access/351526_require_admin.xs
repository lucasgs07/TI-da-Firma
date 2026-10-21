// Require an authenticated user whose perfil_id is the administrator profile (1).
function "helpdesk/access/require_admin" {
  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1) {
      error_type = "accessdenied"
      error = "Administrator access is required."
    }
  }

  response = $actor
}