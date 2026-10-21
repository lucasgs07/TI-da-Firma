// Pull all event logs for the authenticated user
query "logs/user/my_events" verb=GET {
  api_group = "Event Logs"
  auth = "user"

  input {
  }

  stack {
    function.run "helpdesk/access/get_actor_context" as $verified_actor

    // Retrieve event logs for the authenticated user
    db.query event_log {
      where = $db.event_log.user_id == $auth.id
      return = {type: "list"}
    } as $user_events

    // Project the response to safe fields; historical metadata may contain secrets.
    array.map ($user_events) {
      by = {
        id        : $this.id
        created_at: $this.created_at
        user_id   : $this.user_id
        action    : $this.action
      }
    } as $safe_user_events
  }

  response = $safe_user_events
  tags = ["xano:quick-start"]
  guid = "_TKFD55ONwd5YaUmNuzikwh-_Jo"
}
