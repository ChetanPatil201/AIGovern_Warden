import os
from langchain_openai import AzureChatOpenAI
from aigovern_warden.agents.scout import WardenState

def run_policy_jurist(state: WardenState) -> dict:
    """
    Agent 2: Uses LLM to evaluate risks based on the EU AI Act.
    """
    print("--- [AGENT] Jurist: Evaluating Findings against EU AI Act ---")

    # 1. Initialize the 'Brain'
    # This pulls from your .env keys
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
        openai_api_version="2024-02-01",
    )

    # 2. Construct the Audit Prompt
    # We pass the list of findings to the LLM
    findings_str = "\n".join(state["findings"])


    prompt = f"""
    Act as a Lead EU AI Auditor. Perform a 'Gap Analysis' on these Azure findings.

    FINDINGS:
    {findings_str}

    LEGAL BENCHMARK (EU AI ACT 2026):
    1. ARTICLE 10 (Bias): If 'BIAS_WARNING' is present, flag as 'NON-COMPLIANT'. High-risk systems must utilize quality datasets that are representative and free of errors (bias mitigation).
    2. ARTICLE 11 (Documentation): Every AI service needs an 'Annex IV' dossier. Flag 'SDS-LLM' as a priority.
    3. ARTICLE 14 (Human Oversight): Note that all remediation will be handled via GitHub PR to satisfy Human-in-the-Loop requirements.

    OUTPUT:
    Identify the 'Financial Penalty Risk' (based on 7% of turnover) and cite the specific violation.
    """
    
    # 3. Get the Reasoning
    response = llm.invoke(prompt)
    
    # We update the findings with the 'judged' version
    return {"findings": [response.content]}

