query "chamado/{chamado_id}/sugerir-solucao" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    int chamado_id filters=min:1
  }

  stack {
    function.run "helpdesk/access/require_suggestion_ticket" {
      input = {chamado_id: $input.chamado_id}
    } as $ticket_context

    precondition ($env.N8N_SUGGESTION_HEADER_NAME != null && $env.N8N_SUGGESTION_HEADER_NAME != "" && $env.N8N_SUGGESTION_HEADER_VALUE != null && $env.N8N_SUGGESTION_HEADER_VALUE != "") {
      error = "Suggestion service is not configured."
    }

    var $auth_header {
      value = $env.N8N_SUGGESTION_HEADER_NAME|concat:": "|concat:$env.N8N_SUGGESTION_HEADER_VALUE
    }

    api.request {
      url = "https://dgzinl8.app.n8n.cloud/webhook/sugerir-solucao"
      method = "POST"
      params = $ticket_context
      headers = ["Content-Type: application/json", "Accept: application/json", $auth_header]
      timeout = 12
      follow_location = false
    } as $webhook

    precondition ($webhook.response.status == 200 && $webhook.response.result != null && $webhook.response.result != false) {
      error = "Suggestion service is unavailable."
    }

    var $rows {
      value = $webhook.response.result.sugestoes
    }

    precondition ($rows != null) {
      error = "Suggestion service returned an invalid response."
    }

    array.map ($rows) {
      by = {titulo: $this.titulo, passos: $this.passos}
    } as $suggestions
  }

  response = {sugestoes: $suggestions}
}
