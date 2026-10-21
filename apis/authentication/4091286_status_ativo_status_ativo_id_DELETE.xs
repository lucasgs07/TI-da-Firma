// Delete a status_ativo lookup record; only administrators may mutate lookup data.
query "status_ativo/{status_ativo_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int status_ativo_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get status_ativo {
      field_name = "id"
      field_value = $input.status_ativo_id
    } as $status_ativo
  
    precondition ($status_ativo != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del status_ativo {
      field_name = "id"
      field_value = $input.status_ativo_id
    }
  }

  response = null
}