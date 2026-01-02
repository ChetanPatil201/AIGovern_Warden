
### PROPOSED TERRAFORM FIX:
```hcl
resource "azurerm_cognitive_account" "sds_llm" {
  name                = "SDS-LLM"
  location            = "westus"
  resource_group_name = "example-resource-group"
  kind                = "OpenAI"
  sku_name            = "S0"
  properties          = {}
}

resource "azurerm_cognitive_account" "aiboting" {
  name                = "AIBOTING"
  location            = "westus"
  resource_group_name = "example-resource-group"
  kind                = "OpenAI"
  sku_name            = "S0"
  properties          = {}
}
```