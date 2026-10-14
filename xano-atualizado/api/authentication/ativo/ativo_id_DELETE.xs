// Delete ativo record.
query "ativo/{ativo_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int ativo_id? filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $actor
    db.get ativo {
      field_name = "id"
      field_value = $input.ativo_id
    } as $ativo
  
    precondition ($ativo != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del ativo {
      field_name = "id"
      field_value = $input.ativo_id
    }
  }

  response = null
  guid = "pZKsfopRnX-hM8cf5onIBaoh3jg"
}