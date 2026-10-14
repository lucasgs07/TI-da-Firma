// Return a paginated, newest-first global event log for administrators.
query "logs/events" verb=GET {
  api_group = "Event Logs"
  auth = "user"

  input {
    // Page number, starting at 1.
    int page?=1 filters=min:1
  
    // Number of events per page, capped at 100.
    int per_page?=25 filters=min:1|max:100
  }

  stack {
    // The helper resolves the actor from $auth.id and enforces perfil_id 1.
    function.run "helpdesk/access/require_admin" as $admin_actor
  
    db.query event_log {
      sort = {event_log.created_at: "desc"}
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
        "offset"
        "itemsTotal"
        "pageTotal"
        "items.id"
        "items.created_at"
        "items.user_id"
        "items.action"
      ]
    } as $safe_events
  }

  response = $safe_events
  guid = "OjKspk75sqg3fGyAIBnMT4NhvTU"
}