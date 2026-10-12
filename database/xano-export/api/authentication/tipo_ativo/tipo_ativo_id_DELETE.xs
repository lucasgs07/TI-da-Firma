// Delete a tipo_ativo lookup record; only administrators may mutate lookup data.
query "tipo_ativo/{tipo_ativo_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int tipo_ativo_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get tipo_ativo {
      field_name = "id"
      field_value = $input.tipo_ativo_id
    } as $tipo_ativo
  
    precondition ($tipo_ativo != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del tipo_ativo {
      field_name = "id"
      field_value = $input.tipo_ativo_id
    }
  }

  response = null
  guid = "GmqL1nvNq4jcXyZHPilYGBOnRPA"
}