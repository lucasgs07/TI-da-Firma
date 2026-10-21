// Legacy interaction mutation is intentionally disabled by policy.
// Disable legacy interaction deletion; deletion is not authorized by the interaction policy.
query "interacao_chamado/{interacao_chamado_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    // Legacy route ID; deletion is not supported.
    int interacao_chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $verified_actor
    precondition (false) {
      error_type = "accessdenied"
      error = "Interaction deletion is not permitted."
    }
  }

  response = null
  guid = "-ZvBSUjaJcTreiZYCNmMPFW8jmM"
}
