// Login and return an operational session using the user's actual profile fields.
// Authenticate a user with an operational profile and return a safe session projection.
query "auth/login" verb=POST {
  api_group = "Authentication"

  input {
    // Account email address.
    email email filters=trim|lower
  
    // Account password.
    text password filters=min:8 {
      sensitive = true
    }
  }

  stack {
    // Fetch only the credential and operational identity fields needed below.
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id", "name", "email", "password", "perfil_id", "departamento_id"]
    } as $user
  
    precondition ($user != null) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }
  
    precondition ($user.password != null) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }
  
    security.check_password {
      text_password = $input.password
      hash_password = $user.password
    } as $pass_result
  
    precondition ($pass_result) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }
  
    // Do not issue an operational session for accounts with missing or invalid profiles.
    precondition ($user.perfil_id == 1 || $user.perfil_id == 2 || $user.perfil_id == 3 || $user.perfil_id == 4) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }
  
    db.get perfil {
      field_name = "id"
      field_value = $user.perfil_id
      output = ["id"]
    } as $profile
  
    precondition ($profile != null) {
      error_type = "accessdenied"
      error = "Invalid Credentials."
    }
  
    conditional {
      if ($user.perfil_id != 1) {
        precondition ($user.departamento_id != null) {
          error_type = "accessdenied"
          error = "Invalid Credentials."
        }
      }
    }
  
    conditional {
      if ($user.departamento_id != null) {
        db.get departamento {
          field_name = "id"
          field_value = $user.departamento_id
          output = ["id"]
        } as $department
      
        precondition ($department != null) {
          error_type = "accessdenied"
          error = "Invalid Credentials."
        }
      }
    }
  
    // Non-secret session profile; never includes the password hash.
    var $safe_user {
      value = {
        id             : $user.id
        name           : $user.name
        email          : $user.email
        perfil_id      : $user.perfil_id
        departamento_id: $user.departamento_id
      }
    }
  
    security.create_auth_token {
      table = "user"
      extras = {}
      expiration = 86400
      id = $user.id
    } as $authToken
  
    function.run "Quick Start/log_event" {
      input = {
        user_id : $user.id
        action  : "login"
        metadata: {
        perfil_id      : $user.perfil_id
        departamento_id: $user.departamento_id
      }
      }
    } as $event_log
  }

  response = {
    authToken: $authToken
    user_id  : $user.id
    user     : $safe_user
  }

  tags = ["xano:quick-start"]
  history = false
  guid = "atRghE1Z87SqOyCgL1loWL5Uy5o"
}