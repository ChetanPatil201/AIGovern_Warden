
### PROPOSED TERRAFORM FIX:
```hcl
resource "azurerm_cognitive_account" "sds_llm_westus" {
  name                = "sds-llm-westus"
  location            = "westus"
  resource_group_name = "your_resource_group_name" # Replace with your resource group name
  kind                = "OpenAI"
  sku_name            = "S0"

  tags = {
    environment = "production" # Add any required tags
  }
}

resource "azurerm_cognitive_account" "aiboting_westus" {
  name                = "aiboting-westus"
  location            = "westus"
  resource_group_name = "your_resource_group_name" # Replace with your resource group name
  kind                = "OpenAI"
  sku_name            = "S0"

  tags = {
    environment = "production" # Add any required tags
  }
}
```