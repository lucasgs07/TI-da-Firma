// Administrator-only public ticket history, with a stable insertion boundary.
query "helpdesk/tickets/history" verb=GET {
  api_group = "Authentication"
  auth = "user"

  input {
    int? chamado_id? filters=min:1
    int page?=1 filters=min:1
    int per_page?=100 filters=min:1|max:100
    int? through_id? filters=min:0
  }

  stack {
    function.run "helpdesk/access/require_admin" {
      mock = {
        "empty history"         : {id: 10, perfil_id: 1}
        "history keeps boundary": {id: 10, perfil_id: 1}
      }
    } as $admin
  
    conditional {
      if ($input.chamado_id != null) {
        db.get chamado {
          field_name = "id"
          field_value = $input.chamado_id
          output = ["id"]
        } as $ticket
      
        precondition ($ticket != null) {
          error_type = "notfound"
          error = "Ticket not found."
        }
      }
    }
  
    var $boundary {
      value = $input.through_id
    }
  
    conditional {
      if ($boundary == null) {
        var.update $boundary {
          value = 0
        }
      
        db.query interacao_chamado {
          where = ($input.chamado_id == null || $db.interacao_chamado.chamado_id == $input.chamado_id)
          sort = {interacao_chamado.id: "desc"}
          return = {type: "list", paging: {page: 1, per_page: 1}}
          output = ["items.id"]
          mock = {"empty history": {items: []}}
        } as $latest
      
        foreach ($latest.items) {
          each as $last {
            var.update $boundary {
              value = $last.id
            }
          }
        }
      }
    }
  
    db.query interacao_chamado {
      join = {
        author: {
          table: "user"
          type : "left"
          where: $db.interacao_chamado.user_id == $db.author.id
        }
      }
    
      where = ($input.chamado_id == null || $db.interacao_chamado.chamado_id == $input.chamado_id) && $db.interacao_chamado.id <= $boundary
      sort = {
        interacao_chamado.created_at: "asc"
        interacao_chamado.id        : "asc"
      }
    
      eval = {author_name: $db.author.name}
      return = {
        type  : "list"
        paging: {
          page    : $input.page
          per_page: $input.per_page
          totals  : true
        }
      }
    
      output = [
        "itemsReceived"
        "curPage"
        "nextPage"
        "prevPage"
        "itemsTotal"
        "pageTotal"
        "items.id"
        "items.chamado_id"
        "items.created_at"
        "items.user_id"
        "items.author_name"
        "items.mensagem"
      ]
    
      mock = {
        "empty history"         : {items: [], nextPage: null, itemsTotal: 0, pageTotal: 0}
        "history keeps boundary": ```
          {
            items: [{id: 2, chamado_id: 9, created_at: 1000, user_id: null, author_name: null, mensagem: "Olá"}]
            nextPage: null
            itemsTotal: 1
            pageTotal: 1
          }
          ```
      }
    } as $history
  
    var $result {
      value = $history|set:"through_id":$boundary
    }
  }

  response = $result

  test "empty history" {
    input = {page: 1, per_page: 100}
  
    expect.to_equal ($response.through_id) {
      value = 0
    }
  
    expect.to_equal ($response.items) {
      value = []
    }
  }

  test "history keeps boundary" {
    input = {page: 1, per_page: 100, through_id: 2}
  
    expect.to_equal ($response.through_id) {
      value = 2
    }
  
    expect.to_equal ($response.itemsTotal) {
      value = 1
    }
  }

  guid = "qrojGv_ifZF5rsWiZvaMaP3TFug"
}