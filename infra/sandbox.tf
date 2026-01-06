# 1. SETUP & PROVIDER
terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

provider "azurerm" {
  features {}
  subscription_id = "1a317aed-2ae0-467e-a97d-46ea4e51f919"
}

# 2. RESOURCE GROUP (Simulating EU Act Violation in East US)
resource "azurerm_resource_group" "trap" {
  name     = "rg-warden-compliance-trap"
  location = "eastus" 
}

# 3. NETWORKING INFRASTRUCTURE
resource "azurerm_virtual_network" "vnet" {
  name                = "warden-vnet"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.trap.location
  resource_group_name = azurerm_resource_group.trap.name
}

resource "azurerm_subnet" "subnet" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.trap.name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = ["10.0.2.0/24"]
}

# Network Interfaces for our 3 test cases
resource "azurerm_network_interface" "nic_high" {
  name                = "nic-high-risk"
  location            = azurerm_resource_group.trap.location
  resource_group_name = azurerm_resource_group.trap.name
  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_network_interface" "nic_ambiguous" {
  name                = "nic-ambiguous"
  location            = azurerm_resource_group.trap.location
  resource_group_name = azurerm_resource_group.trap.name
  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_network_interface" "nic_generic" {
  name                = "nic-generic"
  location            = azurerm_resource_group.trap.location
  resource_group_name = azurerm_resource_group.trap.name
  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.subnet.id
    private_ip_address_allocation = "Dynamic"
  }
}

# 4. SIGNAL 1: HIGH CERTAINTY VIOLATION (Signal 9-10)
# A GPU machine with a high-risk name.
resource "azurerm_linux_virtual_machine" "high_certainty_ai" {
  name                = "vm-hr-recruitment-gpu"
  resource_group_name = azurerm_resource_group.trap.name
  location            = azurerm_resource_group.trap.location
  size                = "Standard_B2s" # Changed from GPU due to quota limits
  admin_username      = "adminuser"
  network_interface_ids = [azurerm_network_interface.nic_high.id]

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("/Users/poonambhatjire/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

# 5. SIGNAL 2: AMBIGUOUS ASSET (Signal 4-6)
# Standard VM, no GPU, but suggestive name.
resource "azurerm_linux_virtual_machine" "ambiguous_ml" {
  name                = "vm-dev-ml-test-01"
  resource_group_name = azurerm_resource_group.trap.name
  location            = azurerm_resource_group.trap.location
  size                = "Standard_B2s" 
  admin_username      = "adminuser"
  network_interface_ids = [azurerm_network_interface.nic_ambiguous.id]

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("/Users/poonambhatjire/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

# 6. SIGNAL 3: GENERIC NOISE (Signal 1-3)
# Low-cost VM with generic name.
resource "azurerm_linux_virtual_machine" "generic_web" {
  name                = "web-server-01"
  resource_group_name = azurerm_resource_group.trap.name
  location            = azurerm_resource_group.trap.location
  size                = "Standard_B1s"
  admin_username      = "adminuser"
  network_interface_ids = [azurerm_network_interface.nic_generic.id]

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("/Users/poonambhatjire/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}

# 7. AI NATIVE SERVICES (Article 5 & Annex III)
resource "azurerm_cognitive_account" "biometric" {
  name                = "CityScan-Public-Biometrics"
  location            = azurerm_resource_group.trap.location
  resource_group_name = azurerm_resource_group.trap.name
  kind                = "Face"
  sku_name            = "S0"
}

# 8. DATA EXPOSURE & NSG
resource "azurerm_storage_account" "biased_data" {
  name                     = "stwardencustprof001"
  resource_group_name      = azurerm_resource_group.trap.name
  location                 = azurerm_resource_group.trap.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

resource "azurerm_network_security_group" "vulnerable_nsg" {
  name                = "nsg-ai-training-public"
  location            = azurerm_resource_group.trap.location
  resource_group_name = azurerm_resource_group.trap.name

  security_rule {
    name                       = "AllowSSH"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "22"
    source_address_prefix      = "*"
    destination_address_prefix = "*"
  }
}