
### PROPOSED TERRAFORM FIX:
```hcl
resource "azurerm_cognitive_account" "sds_llm" {
  name                = "sds-llm-westus"
  location            = "westus"
  resource_group_name = "rg-sds-llm-westus"
  kind                = "OpenAI"
  sku_name            = "S0"

  tags = {
    environment = "production"
    migration   = "from-eastus"
  }
}

resource "azurerm_cognitive_account" "aiboting" {
  name                = "aiboting-westus"
  location            = "westus"
  resource_group_name = "rg-aiboting-westus"
  kind                = "OpenAI"
  sku_name            = "S0"

  tags = {
    environment = "production"
    migration   = "from-eastus"
  }
}
```