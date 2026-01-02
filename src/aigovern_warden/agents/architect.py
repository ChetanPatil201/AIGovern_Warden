import os
from langchain_openai import AzureChatOpenAI
from aigovern_warden.agents.scout import WardenState

def run_remediation_architect(state: WardenState) -> dict:
    """
    Agent 3: Generates Terraform code to fix compliance issues.
    """
    print("--- [AGENT] Architect: Generating Terraform Remediation ---")
    
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
        openai_api_version="2024-02-01",
    )
    # We take the findings (which now contain the Jurist's audit)
    audit_report = "\n".join(state["findings"])

    prompt = f"""
    You are a Senior Cloud Engineer and Terraform Expert.
    
    Based on this Audit Report:
    {audit_report}
    
    Your Task:
    1. For any resource in 'eastus', generate a Terraform snippet to recreate it in 'westus'.
    2. Use the 'azurerm_cognitive_account' resource type.
    3. Ensure the 'kind' is 'OpenAI' and the 'sku_name' is 'S0'.
    
    Return ONLY the Terraform code wrapped in markdown code blocks.
    """

    response = llm.invoke(prompt)
    
    # We append the Terraform code to our findings
    return {"findings": state["findings"] + ["\n### PROPOSED TERRAFORM FIX:\n" + response.content]}