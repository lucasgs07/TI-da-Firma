// Send a welcome email to an authorized user and record a minimal audit event.
query "message/send_welcome_email" verb=POST {
  api_group = "Authentication"
  auth = "user"

  input {
    // ID of the user who should receive the welcome email.
    int user_id filters=min:1
  }

  stack {
    // Resolve the actor only from the authenticated Xano context.
    function.run "helpdesk/access/get_actor_context" as $actor
  
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Only administrators and managers may send welcome emails."
    }
  
    // Apply the actor's scope in the lookup itself so managers cannot distinguish
    // existing users outside their department or users with ineligible profiles.
    db.query user {
      where = $db.user.id == $input.user_id && ($actor.perfil_id == 1 || ($db.user.departamento_id == $actor.departamento_id && ($db.user.perfil_id == 3 || $db.user.perfil_id == 4)))
      return = {type: "single"}
      output = ["id", "perfil_id"]
    } as $target_profile
  
    precondition ($target_profile != null) {
      error_type = "notfound"
      error = "User not found or not eligible."
    }
  
    function.run "helpdesk/access/authorize_target_user" {
      input = {
        target_user_id    : $target_profile.id
        expected_perfil_id: $target_profile.perfil_id
      }
    } as $authorized_target
  
    // Read recipient details only after the helper has authorized the target.
    db.get user {
      field_name = "id"
      field_value = $authorized_target.id
      output = ["id", "name", "email", "perfil_id", "departamento_id"]
    } as $recipient
  
    precondition ($recipient != null && $recipient.email != null) {
      error_type = "notfound"
      error = "The authorized user does not have a deliverable email address."
    }
  
    var $email_subject {
      value = "Welcome to Our Service, " ~ $recipient.name ~ "!"
    }
  
    var $email_body {
      value = "Welcome, " ~ $recipient.name ~ "!\n\nThank you for joining our service. We're excited to have you!\n\nBest regards,\nThe Team"
    }
  
    util.send_email {
      service_provider = "xano"
      subject = $email_subject
      message = $email_body
      to = $recipient.email
    } as $send_email
  
    db.add event_log {
      data = {
        created_at: now
        user_id   : $actor.id
        action    : "welcome_email_sent"
        metadata  : {
        target_user_id  : $authorized_target.id
        target_perfil_id: $authorized_target.perfil_id
      }
      }
    } as $event_log
  
    var $result {
      value = {
        success: true
        user_id: $authorized_target.id
        action : "welcome_email_sent"
      }
    }
  }

  response = $result
  tags = ["xano:quick-start"]
  history = false
  guid = "0Vor0fuYHYRZ1IwLUtbzmhfYgqA"
}