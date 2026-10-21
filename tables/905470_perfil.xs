table perfil {
  auth = false

  schema {
    int id
    text name? filters=trim
    text? descricao? filters=trim
  }

  index = [{type: "primary", field: [{name: "id"}]}]
}