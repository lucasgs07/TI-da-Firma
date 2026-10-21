// Verify an existing target user has the expected profile and is within the authenticated administrator's or manager's allowed department scope.
function "helpdesk/access/authorize_target_user" {
  input {
    // ID of the user being assigned or managed.
    int target_user_id
  
    // Required target profile ID: 1 Admin, 2 Gestor, 3 Tecnico, or 4 Funcionario.
    int expected_perfil_id filters=min:1|max:4
  }

  stack {
    function.run "helpdesk/access/get_actor_context" {
      mock = {
        "should authorize an administrator target in another department"           : {id: 10, name: "Admin", perfil_id: 1, departamento_id: 2}
        "should authorize an administrator target manager in another department"   : {id: 10, name: "Admin", perfil_id: 1, departamento_id: 2}
        "should authorize an administrator target technician in another department": {id: 10, name: "Admin", perfil_id: 1, departamento_id: 2}
        "should authorize an administrator target employee in another department"  : {id: 10, name: "Admin", perfil_id: 1, departamento_id: 2}
        "should authorize a manager technician in the same department"             : {id: 20, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should authorize a manager employee in the same department"               : {id: 20, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should deny a manager target with admin profile"                          : {id: 20, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should deny a manager target with manager profile"                        : {id: 20, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should deny a manager target in another department"                       : {id: 20, name: "Manager", perfil_id: 2, departamento_id: 7}
        "should deny a target whose profile does not match"                        : {id: 10, name: "Admin", perfil_id: 1, departamento_id: 2}
        "should deny technician actor authorization"                               : {id: 30, name: "Technician", perfil_id: 3, departamento_id: 7}
        "should deny employee actor authorization"                                 : {id: 40, name: "Employee", perfil_id: 4, departamento_id: 7}
      }
    } as $actor
  
    precondition ($actor.perfil_id == 1 || $actor.perfil_id == 2) {
      error_type = "accessdenied"
      error = "Only administrators and managers may authorize target users."
    }
  
    conditional {
      if ($actor.perfil_id == 2) {
        precondition ($input.expected_perfil_id == 3 || $input.expected_perfil_id == 4) {
          error_type = "accessdenied"
          error = "Managers may manage only technicians and employees."
        }
      }
    }
  
    db.get user {
      field_name = "id"
      field_value = $input.target_user_id
      output = ["id", "name", "perfil_id", "departamento_id"]
      mock = {
        "should authorize an administrator target in another department"           : {id: 101, name: "Admin Target", perfil_id: 1, departamento_id: 9}
        "should authorize an administrator target manager in another department"   : {id: 102, name: "Manager Target", perfil_id: 2, departamento_id: 9}
        "should authorize an administrator target technician in another department": {id: 103, name: "Technician Target", perfil_id: 3, departamento_id: 9}
        "should authorize an administrator target employee in another department"  : {id: 104, name: "Employee Target", perfil_id: 4, departamento_id: 9}
        "should authorize a manager technician in the same department"             : {id: 105, name: "Department Technician", perfil_id: 3, departamento_id: 7}
        "should authorize a manager employee in the same department"               : {id: 106, name: "Department Employee", perfil_id: 4, departamento_id: 7}
        "should deny a manager target in another department"                       : {id: 107, name: "Other Department Technician", perfil_id: 3, departamento_id: 8}
        "should deny a target whose profile does not match"                        : {id: 108, name: "Mismatched Target", perfil_id: 4, departamento_id: 2}
      }
    } as $target_user
  
    precondition ($target_user != null) {
      error_type = "notfound"
      error = "Target user was not found."
    }
  
    precondition ($target_user.perfil_id == $input.expected_perfil_id) {
      error_type = "accessdenied"
      error = "Target user does not have the required profile."
    }
  
    conditional {
      if ($actor.perfil_id == 2) {
        precondition ($target_user.departamento_id == $actor.departamento_id) {
          error_type = "accessdenied"
          error = "Managers may manage target users only in their own department."
        }
      }
    }
  
    // Return only non-secret target identity and authorization fields.
    var $authorized_target {
      value = {
        id             : $target_user.id
        name           : $target_user.name
        perfil_id      : $target_user.perfil_id
        departamento_id: $target_user.departamento_id
      }
    }
  }

  response = $authorized_target

  test "should authorize an administrator target in another department" {
    input = {target_user_id: 101, expected_perfil_id: 1}
  
    expect.to_equal ($response) {
      value = {
        id             : 101
        name           : "Admin Target"
        perfil_id      : 1
        departamento_id: 9
      }
    }
  }

  test "should authorize an administrator target manager in another department" {
    input = {target_user_id: 102, expected_perfil_id: 2}
  
    expect.to_equal ($response) {
      value = {
        id             : 102
        name           : "Manager Target"
        perfil_id      : 2
        departamento_id: 9
      }
    }
  }

  test "should authorize an administrator target technician in another department" {
    input = {target_user_id: 103, expected_perfil_id: 3}
  
    expect.to_equal ($response) {
      value = {
        id             : 103
        name           : "Technician Target"
        perfil_id      : 3
        departamento_id: 9
      }
    }
  }

  test "should authorize an administrator target employee in another department" {
    input = {target_user_id: 104, expected_perfil_id: 4}
  
    expect.to_equal ($response) {
      value = {
        id             : 104
        name           : "Employee Target"
        perfil_id      : 4
        departamento_id: 9
      }
    }
  }

  test "should authorize a manager technician in the same department" {
    input = {target_user_id: 105, expected_perfil_id: 3}
  
    expect.to_equal ($response) {
      value = {
        id             : 105
        name           : "Department Technician"
        perfil_id      : 3
        departamento_id: 7
      }
    }
  }

  test "should authorize a manager employee in the same department" {
    input = {target_user_id: 106, expected_perfil_id: 4}
  
    expect.to_equal ($response) {
      value = {
        id             : 106
        name           : "Department Employee"
        perfil_id      : 4
        departamento_id: 7
      }
    }
  }

  test "should deny a manager target with admin profile" {
    input = {target_user_id: 111, expected_perfil_id: 1}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should deny a manager target with manager profile" {
    input = {target_user_id: 112, expected_perfil_id: 2}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should deny a manager target in another department" {
    input = {target_user_id: 107, expected_perfil_id: 3}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should deny a target whose profile does not match" {
    input = {target_user_id: 108, expected_perfil_id: 3}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should deny technician actor authorization" {
    input = {target_user_id: 113, expected_perfil_id: 4}
  
    expect.to_throw {
      exception = ""
    }
  }

  test "should deny employee actor authorization" {
    input = {target_user_id: 114, expected_perfil_id: 3}
  
    expect.to_throw {
      exception = ""
    }
  }
}