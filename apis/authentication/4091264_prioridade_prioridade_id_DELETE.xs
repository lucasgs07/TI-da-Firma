// Delete a prioridade lookup record; only administrators may mutate lookup data.
query "prioridade/{prioridade_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int prioridade_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
    } as $prioridade
  
    precondition ($prioridade != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del prioridade {
      field_name = "id"
      field_value = $input.prioridade_id
    }
  }

  response = null
}