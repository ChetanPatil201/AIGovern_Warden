import os
from typing import List, TypedDict
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
from azure.mgmt.storage import StorageManagementClient

# Load the .env variables
load_dotenv()

# Define the 'Shared Memory' for our Agents
class WardenState(TypedDict):
    findings: List[str]
    subscription_id: str

def run_discovery_scout(state: WardenState) -> dict:
    """
    Agent 1: Scans Azure for 'Shadow AI' signatures.
    """
    print("--- [AGENT] Scout: Initiating Multi-Cloud Discovery ---")
    
    sub_id = os.getenv("AZURE_SUBSCRIPTION_ID")
    credential = DefaultAzureCredential()
    new_findings = []

    # 1. Scan for Azure OpenAI Instances
    cog_client = CognitiveServicesManagementClient(credential, sub_id)
    for account in cog_client.accounts.list():
        if "OpenAI" in str(account.kind):
            new_findings.append(f"AI_SERVICE: {account.name} ({account.location})")

    # 2. Scan for GPU VMs (Hidden AI Training)
    compute_client = ComputeManagementClient(credential, sub_id)
    for vm in compute_client.virtual_machines.list_all():
        size = vm.hardware_profile.vm_size.lower()
        # N-Series VMs are specialized for AI/GPUs
        if "standard_n" in size:
            new_findings.append(f"SHADOW_GPU: {vm.name} (Size: {size})")
    
    # 2. NEW: Deep Data Inspection (Article 10 Check)
    storage_client = StorageManagementClient(credential, sub_id)
    for account in storage_client.storage_accounts.list():
        # We look for "unstructured" data stores likely used for training
        if account.kind in ["StorageV2", "BlobStorage"]:
            new_findings.append(f"DATA_STORE_FOUND: {account.name} (Risk: Potential Training Data)")
            
            # BIAS CHECK: Simulating metadata inspection for sensitive proxies
            # In a real enterprise, we'd use 'Azure Purview' or 'Blob Metadata'
            if any(term in account.name.lower() for term in ["user", "customer", "profile"]):
                new_findings.append(f"BIAS_WARNING: Data store '{account.name}' likely contains PII/Sensitive Proxies.")

    return {"findings": new_findings}