// Delete a perfil lookup record; only administrators may mutate lookup data.
query "perfil/{perfil_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int perfil_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get perfil {
      field_name = "id"
      field_value = $input.perfil_id
    } as $perfil
  
    precondition ($perfil != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del perfil {
      field_name = "id"
      field_value = $input.perfil_id
    }
  }

  response = null
  guid = "qxEFNZv9Myvp_uYDJFryMfMehik"
}