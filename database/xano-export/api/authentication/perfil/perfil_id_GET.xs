// Get a safe perfil lookup record.
query "perfil/{perfil_id}" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int perfil_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $verified_actor
    db.get perfil {
      field_name = "id"
      field_value = $input.perfil_id
    } as $perfil

    precondition ($perfil != null) {
      error_type = "notfound"
      error = "Not Found."
    }

    var $safe_perfil {
      value = {
        id       : $perfil.id
        name     : $perfil.name
        descricao: $perfil.descricao
      }
    }
  }

  response = $safe_perfil
  guid = "dIjF5yjah4mIJ-Li8ABJrLGJ1tY"
}
