import os
from typing import Dict, Any
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

from aigovern_warden.agents.scout import WardenState, run_discovery_scout

# 1. Load configuration from .env
load_dotenv()

def build_warden_engine():
    """
    Architectural Step: Define the Directed Acyclic Graph (DAG).
    This tells LangGraph the order of operations.
    """
    # Initialize the Graph with our State schema
    workflow = StateGraph(WardenState)

    # Add Node: The 'Scout' Agent
    # In LangGraph, a 'Node' is just a function that takes State and returns an update.
    workflow.add_node("discovery_scout", run_discovery_scout)

    # Define Edges: The 'Pathways'
    # We start at START, go to our Scout, and then we are done (for now).
    workflow.add_edge(START, "discovery_scout")
    workflow.add_edge("discovery_scout", END)

    # Compile: This validates the graph and returns a 'Runnable' object.
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