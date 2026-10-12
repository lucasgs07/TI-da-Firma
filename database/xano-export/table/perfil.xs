table perfil {
  auth = false

  schema {
    int id
    text name? filters=trim
    text? descricao? filters=trim
  }

  index = [{type: "primary", field: [{name: "id"}]}]
  guid = "VZ_HVl4jQQEfzho_Ks2HYP31UF4"
}