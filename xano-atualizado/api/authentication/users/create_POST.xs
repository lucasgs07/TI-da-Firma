// Create an account using the authenticated administrator or manager's scope.
// Create a user under administrator or manager permissions, deriving the actor and department from the auth token.
query "users/create" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // New user's full name.
    text name filters=trim|min:1
  
    // New user's unique email address.
    email email filters=trim|lower
  
    // Initial password; the user table enforces minimum length, letter, and digit rules.
    text password filters=min:8 {
      sensitive = true
    }
  
    // Operational profile: 1 Admin, 2 Gestor, 3 Tecnico, or 4 Funcionario.
    int perfil_id filters=min:1|max:4
  
    // Optional requested department for administrators; managers are always assigned to their own department.
    int departamento_id?
  }

  stack {
    util.get_all_input as $provided_input
    function.run "helpdesk/access/get_actor_context" as $actor
  
    // Department selected by an administrator or derived from the authenticated manager.
    var $target_department_id {
      value = null
    }
  
    conditional {
      if ($actor.perfil_id == 1) {
        function.run "helpdesk/access/require_admin" as $admin
        conditional {
          if ($provided_input.departamento_id > 0) {
            var.update $target_department_id {
              value = $provided_input.departamento_id
            }
          }
        }
      }
    
      elseif ($actor.perfil_id == 2) {
        function.run "helpdesk/access/require_manager_department" as $manager_scope
        precondition ($input.perfil_id == 3 || $input.perfil_id == 4) {
          error_type = "accessdenied"
          error = "Managers may create only technicians and employees."
        }
      
        conditional {
          if ($provided_input.departamento_id > 0 && $provided_input.departamento_id != $manager_scope.departamento_id) {
            precondition (false) {
              error_type = "accessdenied"
              error = "Managers may create users only in their own department."
            }
          }
        }
      
        var.update $target_department_id {
          value = $manager_scope.departamento_id
        }
      }
    
      else {
        precondition (false) {
          error_type = "accessdenied"
          error = "Only administrators and managers may create users."
        }
      }
    }
  
    db.get perfil {
      field_name = "id"
      field_value = $input.perfil_id
      output = ["id"]
    } as $target_profile
  
    precondition ($target_profile != null) {
      error_type = "inputerror"
      error = "The requested operational profile does not exist."
    }
  
    precondition ($target_department_id != null || $input.perfil_id == 1) {
      error_type = "inputerror"
      error = "A department is required for non-administrator users."
    }
  
    conditional {
      if ($target_department_id != null) {
        db.get departamento {
          field_name = "id"
          field_value = $target_department_id
          output = ["id"]
        } as $target_department
      
        precondition ($target_department != null) {
          error_type = "inputerror"
          error = "The requested department does not exist."
        }
      }
    }
  
    db.get user {
      field_name = "email"
      field_value = $input.email
      output = ["id"]
    } as $existing_user
  
    precondition ($existing_user == null) {
      error_type = "inputerror"
      error = "An account with this email already exists."
    }
  
    db.add user {
      data = {
        name           : $input.name
        email          : $input.email
        password       : $input.password
        perfil_id      : $input.perfil_id
        departamento_id: $target_department_id
        status         : "Ativo"
      }
    } as $new_user
  
    // Only non-secret user identity and operational fields are returned.
    var $safe_user {
      value = {
        id             : $new_user.id
        name           : $new_user.name
        email          : $new_user.email
        perfil_id      : $new_user.perfil_id
        departamento_id: $new_user.departamento_id
        status         : $new_user.status
      }
    }
  
    function.run "Quick Start/log_event" {
      input = {
        user_id : $actor.id
        action  : "user_created"
        metadata: {
        target_user_id        : $new_user.id
        target_perfil_id      : $new_user.perfil_id
        target_departamento_id: $new_user.departamento_id
      }
      }
    } as $event_log
  }

  response = $safe_user
  history = false
  guid = "_Kt3UhMtVJNkiSVXrJ3OQqLmblY"
}