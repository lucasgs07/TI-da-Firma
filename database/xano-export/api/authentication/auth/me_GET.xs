// Return the safe user profile belonging to the authentication token.
// Return the authenticated user's verified operational profile without credential fields.
query "auth/me" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    db.get perfil {
      field_name = "id"
      field_value = $actor.perfil_id
      output = ["id"]
    } as $profile
  
    precondition ($profile != null) {
      error_type = "accessdenied"
      error = "The authenticated user does not have a recognized profile."
    }
  
    conditional {
      if ($actor.departamento_id != null) {
        db.get departamento {
          field_name = "id"
          field_value = $actor.departamento_id
          output = ["id"]
        } as $department
      
        precondition ($department != null) {
          error_type = "accessdenied"
          error = "The authenticated user's department could not be verified."
        }
      }
    }
  
    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "email", "perfil_id", "departamento_id"]
    } as $user
  
    precondition ($user != null) {
      error_type = "accessdenied"
      error = "The authenticated user could not be verified."
    }
  
    // Safe profile projection; excludes password, password reset data, and token.
    var $safe_user {
      value = {
        id             : $user.id
        name           : $user.name
        email          : $user.email
        perfil_id      : $actor.perfil_id
        departamento_id: $actor.departamento_id
      }
    }
  
    function.run "Quick Start/log_event" {
      input = {
        user_id : $actor.id
        action  : "get_auth_user"
        metadata: {
        perfil_id      : $actor.perfil_id
        departamento_id: $actor.departamento_id
      }
      }
    } as $event_log
  }

  response = $safe_user
  tags = ["xano:quick-start"]
  history = false
  guid = "rBdiH4b3AVKbVmzVvF1IL8O6chU"
}