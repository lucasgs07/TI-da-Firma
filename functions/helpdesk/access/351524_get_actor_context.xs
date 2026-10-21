// Load the authenticated user using only the trusted auth context and return the minimum identity fields needed for authorization.
function "helpdesk/access/get_actor_context" {
  input {
  }

  stack {
    precondition ($auth.id != null) {
      error_type = "accessdenied"
      error = "Authentication is required."
    }

    db.get user {
      field_name = "id"
      field_value = $auth.id
      output = ["id", "name", "perfil_id", "departamento_id", "status"]
    } as $actor

    precondition ($actor != null) {
      error_type = "accessdenied"
      error = "The authenticated user could not be verified."
    }

    precondition ($actor.status != "Inativo") {
      error_type = "unauthorized"
      error = "Account is inactive."
    }

    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2 || $actor.perfil_id == 3 || $actor.perfil_id == 4) {
      error_type = "accessdenied"
      error = "The authenticated user does not have a recognized profile."
    }

    conditional {
      if ($actor.perfil_id != 1) {
        precondition ($actor.departamento_id != null) {
          error_type = "accessdenied"
          error = "A department is required for this user profile."
        }

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

    // Minimal authenticated identity; does not include email, password, or other secrets.
    var $actor_context {
      value = {
        id             : $actor.id
        name           : $actor.name
        perfil_id      : $actor.perfil_id
        departamento_id: $actor.departamento_id
      }
    }
  }

  response = $actor_context
  guid = "W_HfzgLdH49j0V4xKK4CnHYGeWg"
}
