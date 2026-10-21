// Ticket deletion is disabled: no profile has been granted a ticket-delete permission.
// Disable ticket deletion. No ticket deletion permission has been approved.
query "chamado/{chamado_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    // Ticket ID from the route; retained for route compatibility.
    int chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition (false) {
      error_type = "accessdenied"
      error = "Ticket deletion is not available."
    }
  }

  response = null
}