// Allows user to update the password in the password reset flow
query "reset/update_password" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    text password? filters=trim|min:8
    text confirm_password? filters=trim
  }

  stack {
    // Require both optional inputs before comparing or persisting them
    precondition ($input.password != null && ($input.password|strlen) > 0 && $input.confirm_password != null && ($input.confirm_password|strlen) > 0) {
      error = "Password and confirmation are required."
    }
  
    // Check that the password inputs are matching
    precondition ($input.password == $input.confirm_password) {
      error = "Passwords do not match!"
    }
  
    // Get user record based on the id of the auth token
    db.get user {
      field_name = "id"
      field_value = $auth.id
    } as $user
  
    // Check that the user record id matches the auth id
    precondition ($user.id == $auth.id) {
      error_type = "accessdenied"
    }
  
    // Update user record with the new password
    db.edit user {
      field_name = "id"
      field_value = $auth.id
      data = {password: $input.password}
    } as $user
  
    // Create event log
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "reset_password"
        metadata: {user_id: $user.id, action: "password_updated"}
      }
    } as $event_log
  }

  response = {
    message: {"success":"true","message":"Password updated"}
  }

  tags = ["xano:quick-start"]
  history = false
}