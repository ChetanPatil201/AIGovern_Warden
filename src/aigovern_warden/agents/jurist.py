import os
from langchain_openai import AzureChatOpenAI
from aigovern_warden.agents.scout import WardenState

def load_policy_context():
    """Helper to read our 'Knowledge Base' for the EU AI Act."""
    path = "src/aigovern_warden/knowledge/eu_ai_act_summary.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "No policy context available."

def run_policy_jurist(state: WardenState) -> dict:
    """
    Agent 2: Calibrated Jurist. Matches legal confidence to evidence signal strength,
    with an escalation path for Article 51 Systemic Risk models.
    """
    print("--- [AGENT] Jurist: Performing Calibrated Article 51 Audit ---")
    
    # 1. Load the Legal Framework
    legal_context = load_policy_context()

    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
        openai_api_version="2024-02-01",
    )

    findings_str = "\n".join(state["findings"])
    
    # 2. THE CALIBRATED PROMPT: INJECTING SYSTEMIC RISK PRIORITIZATION
    prompt = f"""
    You are a Regulatory Audit Engine designed for the 2026 EU AI Act enforcement. 
    You must match your confidence to the strength of the evidence to avoid "Audit Drift."

    [LEGAL CONTEXT - EU AI ACT 2026]
    {legal_context}

    [INFRASTRUCTURE & MODEL FINDINGS]
    {findings_str}

    AUDIT PROTOCOL & ESCALATION RULES:
    1. SYSTEMIC RISK PRIORITY (Article 51):
       - If a finding contains "SYSTEMIC_RISK: YES", assign a Signal Strength of 10.
       - These models (e.g., GPT-4 class) trigger immediate Article 51 obligations.
    2. SOVEREIGNTY DRIFT:
       - If an AI_RESOURCE has "DRIFT_DETECTED" and "SYSTEMIC_RISK: YES", flag as 'CRITICAL_SOVEREIGNTY_BREACH'.
    3. SHADOW AI:
       - Correlate SHADOW_GPU with Article 11 (Lack of Technical Documentation).

    STEP 1: EVALUATE EVIDENCE SIGNAL (1-10)
    - 10: Explicit resource (OpenAI Service/GPU) + SYSTEMIC_RISK: YES.
    - 7-9: Explicit AI service but no systemic risk or explicit shadow hardware.
    - 4-6: Ambiguous asset with suggestive metadata (e.g., storage with 'data' keywords).
    - 1-3: Generic asset (B-series VM/Standard Storage) with no AI signal.

    STEP 2: BRANCHING VERDICT
    - IF SIGNAL >= 7: Emit CATEGORICAL VERDICT. Cite specific [REF-XX] and legal article.
    - IF SIGNAL 4-6: Emit POTENTIAL RISK. Request specific documentation. Do NOT cite articles as 'violated'.
    - IF SIGNAL < 4: Emit AMBIGUOUS ASSET. Mark as 'Unclassified'.

    OUTPUT FORMAT (JSON-LIKE ARRAY):
    [
      {{
        "Resource": "[Name]",
        "Signal Strength": [1-10],
        "Verdict": "[Categorical / Potential / Ambiguous]",
        "Legal Citation": "[Article XX or N/A]",
        "Reasoning": "[Explain specific signal logic, mention systemic risk if applicable]"
      }}
    ]
    """

    response = llm.invoke(prompt)
    
    # We return the new 'Calibrated Findings' for the Reporter
    return {"findings": [response.content]}