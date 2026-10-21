// Administrative user editing. Credential and identity fields are never writable here.
query "users/{user_id}" verb=PATCH {
  api_group = "Authentication"
  auth = "user"

  input {
    int user_id filters=min:1
    text name filters=trim|min:1
    email email filters=trim|lower
    int perfil_id filters=min:1|max:4
    int departamento_id?
    text status filters=trim
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    util.get_all_input as $provided
    foreach ($provided|keys) {
      each as $field {
        precondition ($field == "user_id" || $field == "name" || $field == "email" || $field == "perfil_id" || $field == "departamento_id" || $field == "status") {
          error_type = "inputerror"
          error = "Unsupported user field."
        }
      }
    }

    precondition ($input.status == "Ativo" || $input.status == "Inativo") {
      error_type = "inputerror"
      error = "Invalid account status."
    }

    db.get perfil {
      field_name = "id"
      field_value = $input.perfil_id
      output = ["id"]
    } as $profile

    precondition ($profile != null) {
      error_type = "inputerror"
      error = "Invalid profile."
    }

    precondition ($input.perfil_id != 3 || $input.departamento_id == 1) {
      error_type = "inputerror"
      error = "Technicians must belong to TI."
    }

    precondition ($input.perfil_id == 1 || $input.departamento_id > 0) {
      error_type = "inputerror"
      error = "Department is required."
    }

    var $target_department_id {
      value = null
    }

    conditional {
      if ($input.departamento_id > 0) {
        var.update $target_department_id {
          value = $input.departamento_id
        }

        db.get departamento {
          field_name = "id"
          field_value = $input.departamento_id
          output = ["id"]
        } as $department

        precondition ($department != null) {
          error_type = "inputerror"
          error = "Invalid department."
        }
      }
    }

    db.transaction {
      stack {
        // A shared, existing profile row serializes ALL administrative user edits.
        // Runtime lock support and concurrent behavior must be verified before publication.
        db.get perfil {
          field_name = "id"
          field_value = 1
          lock = true
          output = ["id"]
        } as $admin_lock

        precondition ($admin_lock != null) {
          error_type = "inputerror"
          error = "Administrator profile is unavailable."
        }

        function.run "helpdesk/access/require_admin" as $current_admin
        db.get user {
          field_name = "id"
          field_value = $input.user_id
          output = ["id", "perfil_id", "status"]
        } as $target

        precondition ($target != null) {
          error_type = "notfound"
          error = "User not found."
        }

        db.query user {
          where = $db.user.email == $input.email && $db.user.id != $input.user_id
          return = {type: "exists"}
        } as $duplicate

        precondition ($duplicate == false) {
          error_type = "inputerror"
          error = "Email is already in use."
        }

        conditional {
          if ($target.perfil_id == 1 && $target.status != "Inativo" && ($input.perfil_id != 1 || $input.status == "Inativo")) {
            db.query user {
              where = $db.user.perfil_id == 1 && ($db.user.status == null || $db.user.status == "" || $db.user.status == "Ativo") && $db.user.id != $input.user_id
              return = {type: "exists"}
            } as $another_admin

            precondition ($another_admin) {
              error_type = "inputerror"
              error = "The last active administrator cannot be disabled or demoted."
            }
          }
        }

        db.edit user {
          field_name = "id"
          field_value = $input.user_id
          data = {
            name           : $input.name
            email          : $input.email
            perfil_id      : $input.perfil_id
            departamento_id: $target_department_id
            status         : $input.status
          }

          output = ["id", "name", "email", "perfil_id", "departamento_id", "status"]
        } as $updated
      }
    }
  }

  response = $updated
  history = false
  guid = "P03JCWEQlrUDq2nP7ip8o6uGcOs"
}
