// Resolve the minimal ticket context after verifying operational access.
function "helpdesk/access/require_suggestion_ticket" {
  input {
    int chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor
    precondition ($actor.perfil_id == 3) {
      error_type = "accessdenied"
      error = "Only technicians may request suggestions."
    }

    db.get chamado {
      field_name = "id"
      field_value = $input.chamado_id
      output = ["id", "titulo", "descricao", "status_chamado_id", "responsavel_id"]
    } as $ticket

    precondition ($ticket != null) {
      error_type = "notfound"
      error = "Ticket was not found."
    }

    db.query chamado_tecnico {
      where = $db.chamado_tecnico.chamado_id == $ticket.id
      return = {type: "list"}
      output = ["tecnico_id"]
    } as $assignments

    array.has ($assignments) if ($this.tecnico_id == $actor.id) as $assigned
    precondition ($assigned || (($assignments|count) == 0 && $ticket.responsavel_id == $actor.id)) {
      error_type = "accessdenied"
      error = "Only an assigned technician may request suggestions."
    }

    db.get status_chamado {
      field_name = "id"
      field_value = $ticket.status_chamado_id
      output = ["nome"]
    } as $status

    precondition ($status != null && ($status.nome == "Aberto" || $status.nome == "Em Análise" || $status.nome == "Em atendimento" || $status.nome == "Aguardando usuário")) {
      error_type = "accessdenied"
      error = "Suggestions require an editable ticket."
    }
  }

  response = {chamado_id: $ticket.id, titulo: $ticket.titulo, descricao: $ticket.descricao}
}
