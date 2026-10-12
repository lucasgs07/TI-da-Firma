// Legacy interaction mutation is intentionally disabled by policy.
// Disable legacy interaction edits; replies must be created through the authorized POST route.
query "interacao_chamado/{interacao_chamado_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    // Legacy route ID; edits are not supported.
    int interacao_chamado_id filters=min:1
  }

  stack {
    precondition (false) {
      error_type = "accessdenied"
      error = "Interaction edits are not permitted."
    }
  }

  response = null
  guid = "u6tm4AxL9YTbGYoQe3BpJwNAl5o"
}