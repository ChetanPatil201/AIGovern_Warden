import os
from langchain_openai import AzureChatOpenAI
from aigovern_warden.agents.scout import WardenState

def run_remediation_architect(state: WardenState) -> dict:
    """
    Agent 3: Generates both Terraform migration code and mandatory 
    Annex IV Technical Dossiers for Article 11 compliance.
    """
    print("--- [AGENT] Architect: Generating Multi-Layer Remediation ---")
    
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
        openai_api_version="2024-02-01",
    )
    
    audit_report = "\n".join(state["findings"])

    prompt = f"""
    You are a Senior AI Compliance Engineer. 
    Review these high-risk findings (Signal >= 7):
    {audit_report}
    
    REMEDIATION TASK:
    1. TERRAFORM: Provide code to migrate 'eastus' resources to 'westus'.
    2. ARTICLE 11 COMPLIANCE: For any system with Signal >= 7 (e.g., SDS-LLM, AIBOTING), 
       generate a 'MANDATORY ANNEX IV TECHNICAL DOSSIER' outline.
    3. INCLUDE: Purpose, Model logic, and Article 14 Human Oversight mechanisms.
    
    Format findings as: 
    ### 🏗️ TERRAFORM REMEDIATION
    [Code]
    ### 📄 ARTICLE 11 TECHNICAL DOSSIER
    [Dossier Content]
    """

    response = llm.invoke(prompt)
    return {"findings": state["findings"] + ["\n" + response.content]}