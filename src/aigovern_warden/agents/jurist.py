import os
from langchain_openai import AzureChatOpenAI
from aigovern_warden.agents.scout import WardenState

def load_policy_context():
    """Reads the 'Knowledge Base' for the EU AI Act context."""
    path = "src/aigovern_warden/knowledge/eu_ai_act_summary.txt"
    if os.path.exists(path):
        with open(path, "r") as f:
            return f.read()
    return "No policy context available."

def run_policy_jurist(state: WardenState) -> dict:
    """
    Agent 2: v2.1 Jurist. Establishes subscription-wide precedents to ensure 
    semantic coherence across similar assets.
    """
    print("--- [AGENT] Jurist: Executing Coherent Precedent Audit ---")
    
    legal_context = load_policy_context()
    llm = AzureChatOpenAI(
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        openai_api_key=os.getenv("AZURE_OPENAI_KEY"),
        openai_api_version="2024-02-01",
    )

    findings_str = "\n".join(state["findings"])
    
    # NEW: v2.1 Protocol forcing semantic consistency
    prompt = f"""
    You are a Lead AI Regulatory Auditor for the EU AI Act 2026. 
    You must ensure 'Decision Coherence'—semantically similar cases must receive consistent verdicts.

    [LEGAL CONTEXT]
    {legal_context}

    [INFRASTRUCTURE FINDINGS]
    {findings_str}

    AUDIT PROTOCOL v2.1:
    1. PHASE 1: PRECEDENT MAPPING
       - Identify semantic clusters (e.g., all resources starting with 'SDS' or 'Recruit').
       - Establish a 'Risk Precedent' for the cluster based on Annex III (High-Risk).
    2. PHASE 2: CALIBRATED SIGNAL (1-10)
       - 10: Explicit Biometrics (Art 5) or Systemic GPAI (Art 51).
       - 7-9: Explicit High-Risk cluster member (e.g., SDS-LLM).
       - 4-6: Ambiguous member of a high-risk cluster (e.g., SDS-Storage).
       - 1-3: Generic resource with no cluster alignment.
    3. PHASE 3: BRANCHING VERDICT
       - SIGNAL >= 7: CATEGORICAL. Cite specific Article.
       - SIGNAL 4-6: POTENTIAL. Request Article 11 Technical Documentation.
       - SIGNAL < 4: AMBIGUOUS. Mark as 'Unclassified'.

    OUTPUT SCHEMA (Strict JSON Array):
    [
      {{
        "Resource": "Name",
        "Signal Strength": 1-10,
        "Verdict": "Categorical/Potential/Ambiguous",
        "Legal Citation": "Article XX",
        "Reasoning": "Explain based on precedent mapping."
      }}
    ]
    """

    response = llm.invoke(prompt)
    return {"findings": [response.content]}