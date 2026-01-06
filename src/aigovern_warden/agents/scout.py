import os
from typing import List, TypedDict
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient

# Load the .env variables
load_dotenv()

class WardenState(TypedDict):
    findings: List[str]
    subscription_id: str

def run_discovery_scout(state: WardenState) -> dict:
    """
    Agent 1: Deep Scout. Merged with recursive Model Inventory and Systemic Risk identification.
    """
    print("--- [AGENT] Scout: Deep Property, Network, & Model Inventory Scan ---")
    
    sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    credential = DefaultAzureCredential()
    new_findings = []

    # 1. AI NATIVE SERVICES (Including Recursive Model Scan for Article 51)
    cog_client = CognitiveServicesManagementClient(credential, sub_id)
    for account in cog_client.accounts.list():
        # Heuristic: Article 10 Sovereignty Check
        region_status = "SOVEREIGN" if "europe" in account.location.lower() else "DRIFT_DETECTED"
        
        if any(ai_type in account.kind for ai_type in ["OpenAI", "Face", "ComputerVision"]):
            new_findings.append(
                f"AI_RESOURCE: {account.name} | KIND: {account.kind} | "
                f"REGION: {account.location} ({region_status}) | SKU: {account.sku.name}"
            )

            # --- RECURSIVE MODEL INVENTORY ---
            if "OpenAI" in account.kind:
                try:
                    rg_name = account.id.split("resourceGroups/")[1].split("/")[0]
                    deployments = cog_client.deployments.list(rg_name, account.name)
                    
                    for dep in deployments:
                        # Logic: Identify Systemic Risk Models (GPT-4 class) per Article 51
                        # Models like GPT-4 require higher transparency and risk reporting
                        is_systemic = "YES" if "gpt-4" in dep.model.name.lower() else "NO"
                        capacity = dep.sku.capacity if dep.sku else "N/A"
                        
                        new_findings.append(
                            f"  └─ MODEL_DEPLOYMENT: {dep.model.name} (v{dep.model.version}) | "
                            f"SYSTEMIC_RISK: {is_systemic} | CAPACITY: {capacity} TPM"
                        )
                except Exception as e:
                    new_findings.append(f"  └─ [RECURSION_ERROR] Access denied to deployment metadata: {str(e)}")

    # 2. INFRASTRUCTURE AI (GPU Identification + Tagging Audit)
    compute_client = ComputeManagementClient(credential, sub_id)
    for vm in compute_client.virtual_machines.list_all():
        size = vm.hardware_profile.vm_size.lower()
        tags = vm.tags if vm.tags else {}
        
        if "standard_n" in size:
            tag_status = "GOVERNED" if "Owner" in tags or "ProjectID" in tags else "SHADOW_AI"
            new_findings.append(
                f"SHADOW_GPU: {vm.name} | SIZE: {size} | STATUS: {tag_status} | "
                f"OS: {vm.storage_profile.os_disk.os_type}"
            )

    # 3. DATA ASSETS (Article 10 Bias & Residency Check)
    storage_client = StorageManagementClient(credential, sub_id)
    for account in storage_client.storage_accounts.list():
        if account.kind in ["StorageV2", "BlobStorage"]:
            public_risk = "PUBLIC_ACCESS_ENABLED" if account.allow_blob_public_access else "PRIVATE"
            bias_risk = "HIGH (Sensitive Proxy Found)" if any(term in account.name.lower() for term in ["user", "customer", "profile", "identity"]) else "LOW"
            
            new_findings.append(
                f"DATA_STORE: {account.name} | REGION: {account.primary_location} | "
                f"BIAS_RISK: {bias_risk} | ACCESS: {public_risk}"
            )
    
    # 4. NETWORK SECURITY AUDIT (Article 15 Compliance)
    network_client = NetworkManagementClient(credential, sub_id)
    for ip in network_client.public_ip_addresses.list_all():
        resource_id = ip.id
        rg_name = resource_id.split("resourceGroups/")[1].split("/")[0] if "resourceGroups/" in resource_id else "Unknown"

        if any(keyword in rg_name.lower() for keyword in ["warden", "ai", "trap"]):
            new_findings.append(f"NETWORK_EXPOSURE: Public IP '{ip.name}' found at {ip.ip_address} in RG: {rg_name}")

    for nsg in network_client.network_security_groups.list_all():
        nsg_rg = nsg.id.split("resourceGroups/")[1].split("/")[0]
        for rule in nsg.security_rules:
            if rule.access == "Allow" and str(rule.destination_port_range) in ["22", "3389", "80", "443"]:
                if any(k in nsg_rg.lower() for k in ["ai", "gpu", "trap"]):
                    new_findings.append(f"SECURITY_GAP: NSG '{nsg.name}' allows {rule.protocol} on port {rule.destination_port_range}.")

    return {"findings": new_findings}