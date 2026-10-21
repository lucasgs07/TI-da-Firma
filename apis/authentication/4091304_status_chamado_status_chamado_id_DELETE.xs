// Delete a status_chamado lookup record; only administrators may mutate lookup data.
query "status_chamado/{status_chamado_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int status_chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get status_chamado {
      field_name = "id"
      field_value = $input.status_chamado_id
    } as $status_chamado
  
    precondition ($status_chamado != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del status_chamado {
      field_name = "id"
      field_value = $input.status_chamado_id
    }
  }

  response = null
}