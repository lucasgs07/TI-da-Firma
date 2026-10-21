// Read a safe user record for administrative management only.
query "users/{user_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int user_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get user {
      field_name = "id"
      field_value = $input.user_id
      output = ["id", "name", "email", "perfil_id", "departamento_id", "status"]
    } as $target_user

    precondition ($target_user != null) {
      error_type = "notfound"
      error = "User not found."
    }
  }

  response = $target_user
  history = false
  guid = "jTttY_2BzLscYaT23zV1F66pCU4"
}
