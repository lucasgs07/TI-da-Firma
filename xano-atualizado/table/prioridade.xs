table prioridade {
  auth = false

  schema {
    int id
    text nome? filters=trim
    int nivel?
  }

  index = [{type: "primary", field: [{name: "id"}]}]
  guid = "LN4VHduTs9IO_VluQcoaOHB-l8Y"
}