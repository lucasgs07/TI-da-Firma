// Return documented solutions from tickets the authenticated actor may read.
query "solucoes-por-categoria" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int categoria_id
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $actor

    db.query chamado {
      join = {
        requester: {
          table: "user"
          type : "left"
          where: $db.chamado.solicitante_id == $db.requester.id
        }
      }

      where = (($actor.perfil_id == 1) || ($actor.perfil_id == 2 && ($actor.departamento_id == 1 || $db.chamado.solicitante_id == $actor.id || ($db.requester.perfil_id == 4 && $db.requester.departamento_id == $actor.departamento_id))) || ($actor.perfil_id == 3) || ($actor.perfil_id == 4 && $db.chamado.solicitante_id == $actor.id)) && $db.chamado.categoria_chamado_id == $input.categoria_id && $db.chamado.solucao_final != null && $db.chamado.solucao_final != "" && $db.chamado.resolvido_em != null
      sort = {chamado.created_at: "desc"}
      return = {type: "list"}
      output = ["id", "solucao_final"]
    } as $solutions
  }

  response = $solutions
  guid = "STLEfbm-4XiJb2VMgk-CUM2Omvo"
}
