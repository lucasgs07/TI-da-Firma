// Keep the legacy signup route but disable it for every caller.
// Public signup is disabled. Use the authenticated user provisioning endpoint.
query "auth/signup" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    precondition (false) {
      error_type = "accessdenied"
      error = "Public signup is disabled."
    }
  }

  response = null
  tags = ["xano:quick-start"]
  history = false
  guid = "hvGiENkKo_C1-M8aVUTlbcd_X-E"
}