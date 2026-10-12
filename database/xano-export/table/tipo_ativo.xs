table tipo_ativo {
  auth = false

  schema {
    int id
    text nome? filters=trim
    text? descricao? filters=trim
  }

  index = [{type: "primary", field: [{name: "id"}]}]
  guid = "GMcNp8Q6RfBJV8NIep7SNW3kqhQ"
}