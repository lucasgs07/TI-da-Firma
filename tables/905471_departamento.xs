table departamento {
  auth = false

  schema {
    int id
    text nome? filters=trim
  }

  index = [{type: "primary", field: [{name: "id"}]}]
}