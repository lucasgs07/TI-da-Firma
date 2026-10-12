// Delete a categoria_chamado lookup record; only administrators may mutate lookup data.
query "categoria_chamado/{categoria_chamado_id}" verb=DELETE {
  api_group = "Authentication"
  auth = "user"

  input {
    int categoria_chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_admin" as $admin
    db.get categoria_chamado {
      field_name = "id"
      field_value = $input.categoria_chamado_id
    } as $categoria_chamado
  
    precondition ($categoria_chamado != null) {
      error_type = "notfound"
      error = "Not Found."
    }
  
    db.del categoria_chamado {
      field_name = "id"
      field_value = $input.categoria_chamado_id
    }
  }

  response = null
  guid = "fnbKtzQyZkYuLQx4muh2y3QDvCU"
}