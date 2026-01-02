import os
from typing import Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from aigovern_warden.agents.scout import WardenState, run_discovery_scout
from aigovern_warden.agents.jurist import run_policy_jurist
from aigovern_warden.agents.architect import run_remediation_architect
from aigovern_warden.agents.git_agent import run_github_agent
from aigovern_warden.agents.reporter import run_reporting_agent

# 1. Load configuration from .env
load_dotenv()

def build_warden_engine():
    workflow = StateGraph(WardenState)

    # Add Nodes
    workflow.add_node("discovery_scout", run_discovery_scout)
    workflow.add_node("policy_jurist", run_policy_jurist) 
    workflow.add_node("remediation_architect", run_remediation_architect)
    workflow.add_node("github_agent", run_github_agent)
    workflow.add_node("reporting_agent", run_reporting_agent)

    # Define the Flow (The Edge Logic)
    workflow.add_edge(START, "discovery_scout")
    workflow.add_edge("discovery_scout", "policy_jurist") 
    workflow.add_edge("policy_jurist", "remediation_architect")
    #workflow.add_edge("remediation_architect", "github_agent")
    #workflow.add_edge("github_agent", "reporting_agent")
    workflow.add_edge("remediation_architect", "reporting_agent")
    workflow.add_edge("reporting_agent", END)

    return workflow.compile()

def main():
    print("=== AIGovern Warden: System Boot ===")
    
    # Initialize the engine
    warden_app = build_warden_engine()
    
    # 2. Set the Initial Input
    # We pull the Subscription ID from our .env vault.
    initial_input = {
        "subscription_id": os.getenv("AZURE_SUBSCRIPTION_ID"),
        "findings": []
    }

    # 3. Invoke the Graph
    # .invoke() is synchronous. For a CLI tool, this is perfect.
    print(f"Targeting Azure Subscription: {initial_input['subscription_id']}\n")
    
    try:
        final_state = warden_app.invoke(initial_input)
        
        # 4. Process the Output
        print("\n=== FINAL DISCOVERY REPORT ===")
        if not final_state['findings']:
            print("✅ No Shadow AI or GPU sprawl detected.")
        else:
            for report in final_state['findings']:
                print(f"🚨 {report}")
                
    except Exception as e:
        print(f"❌ System Error during scan: {str(e)}")

if __name__ == "__main__":
    main()