// Delete a departamento lookup record; only administrators may mutate lookup data.
query "departamento/{departamento_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int departamento_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get departamento {
      field_name = "id"
      field_value = $input.departamento_id
    } as $departamento
  
    precondition ($departamento != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del departamento {
      field_name = "id"
      field_value = $input.departamento_id
    }
  }

  response = null
  guid = "QkIFA3qkyCcAqpic5ltSMOSYQ6s"
}