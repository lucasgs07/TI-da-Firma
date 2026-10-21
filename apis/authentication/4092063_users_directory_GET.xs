// List users for authorized user management and task assignment selectors.
// Return a paginated safe user directory to administrators and managers, including only identity and operational selection fields.
query "users/directory" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    // Optional department filter for administrators; managers may provide only their authenticated department.
    int departamento_id?

    // Optional operational profile filter: 1 Admin, 2 Gestor, 3 Tecnico, or 4 Funcionario.
    int perfil_id?

    // Page number, starting at 1.
    int page?=1 filters=min:1

    // Number of users per page, up to 100.
    int per_page?=50 filters=min:1|max:100
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Only administrators and managers may access the user directory."
    }

    // Absent optional integers arrive as 0 on this instance; treat any value below 1 as no filter.
    var $dept_filter {
      value = null
    }

    var $perfil_filter {
      value = null
    }

    conditional {
      if ($input.departamento_id != null && $input.departamento_id > 0) {
        var.update $dept_filter {
          value = $input.departamento_id
        }
      }
    }

    conditional {
      if ($input.perfil_id != null && $input.perfil_id > 0) {
        var.update $perfil_filter {
          value = $input.perfil_id
        }
      }
    }

    precondition ($perfil_filter == null || $perfil_filter <= 4) {
      error_type = "inputerror"
      error = "The requested operational profile does not exist."
    }

    conditional {
      if ($dept_filter != null && ($actor.perfil_id == 1 || ($actor.perfil_id == 2 && $actor.departamento_id == 1))) {
        db.get departamento {
          field_name = "id"
          field_value = $dept_filter
          output = ["id"]
        } as $requested_department

        precondition ($requested_department != null) {
          error_type = "inputerror"
          error = "The requested department does not exist."
        }
      }
    }

    conditional {
      if ($perfil_filter != null) {
        db.get perfil {
          field_name = "id"
          field_value = $perfil_filter
          output = ["id"]
        } as $requested_profile

        precondition ($requested_profile != null) {
          error_type = "inputerror"
          error = "The requested operational profile does not exist."
        }
      }
    }

    // Administrators search globally; managers are always pinned to their trusted department.
    var $scope_department {
      value = $dept_filter
    }

    conditional {
      if ($actor.perfil_id == 2 && $actor.departamento_id != 1) {
        function.run "helpdesk/access/require_manager_department" as $manager_scope
        precondition ($dept_filter == null || $dept_filter == $manager_scope.departamento_id) {
          error_type = "accessdenied"
          error = "Managers may view users only in their own department."
        }

        var.update $scope_department {
          value = $manager_scope.departamento_id
        }
      }
    }

    conditional {
      if ($actor.perfil_id == 2 && $actor.departamento_id != 1) {
        precondition ($perfil_filter == null || $perfil_filter == 4) {
          error_type = "accessdenied"
          error = "Department managers may select only employees."
        }

        var.update $perfil_filter {
          value = 4
        }
      }
    }

    // Keep email out of the manager/task-assignment projection.
    var $user_rows {
      value = {}
    }

    conditional {
      if ($actor.perfil_id == 1) {
        db.query user {
          where = ($db.user.departamento_id ==? $scope_department) && ($db.user.perfil_id ==? $perfil_filter) && ($actor.perfil_id == 1 || $db.user.perfil_id != 1)
          sort = {user.name: "asc", user.id: "asc"}
          return = {
            type  : "list"
            paging: {
              page    : $input.page
              per_page: $input.per_page
              totals  : true
            }
          }

          output = [
            "itemsReceived"
            "curPage"
            "nextPage"
            "prevPage"
            "offset"
            "itemsTotal"
            "pageTotal"
            "items.id"
            "items.name"
            "items.email"
            "items.perfil_id"
            "items.departamento_id"
            "items.status"
          ]
        } as $admin_rows

        var.update $user_rows {
          value = $admin_rows
        }
      }

      else {
        db.query user {
          where = ($db.user.departamento_id ==? $scope_department) && ($db.user.perfil_id ==? $perfil_filter) && ($actor.perfil_id == 1 || $db.user.perfil_id != 1)
          sort = {user.name: "asc", user.id: "asc"}
          return = {
            type  : "list"
            paging: {
              page    : $input.page
              per_page: $input.per_page
              totals  : true
            }
          }

          output = [
            "itemsReceived"
            "curPage"
            "nextPage"
            "prevPage"
            "offset"
            "itemsTotal"
            "pageTotal"
            "items.id"
            "items.name"
            "items.perfil_id"
            "items.departamento_id"
            "items.status"
          ]
        } as $manager_rows

        var.update $user_rows {
          value = $manager_rows
        }
      }
    }
  }

  response = $user_rows
  history = false
  guid = "Yy6Q7HNRSbzE_3RViB0GEQfpkJg"
}
