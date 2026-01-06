import os
import re
from datetime import datetime
from aigovern_warden.agents.scout import WardenState

def run_reporting_agent(state: WardenState) -> dict:
    print("--- [AGENT] Reporter: Final Calibration & Scoring ---")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sub_id = state.get("subscription_id", "Unknown")
    # Convert list of findings to one giant string for searching
    findings_str = str(state.get("findings", [])) 
    
    # 1. ROBUST PARSING: Extract signal values from Markdown or JSON formats
    # Matches "Signal Strength: 10", "Signal Strength": 10, "**Signal Strength**: 10", etc.
    all_signals = [int(s) for s in re.findall(r"(?:Signal Strength|Signal Strength\")[:\s\*]*(\d+)", findings_str)]
    
    # 2. DETERMINISTIC MATH
    total_assets = len(all_signals)
    critical_violations = sum(1 for s in all_signals if s >= 9)
    high_risk_violations = sum(1 for s in all_signals if 7 <= s <= 8)
    ambiguous_assets = sum(1 for s in all_signals if 4 <= s <= 6)
    
    # Mathematical Readiness Score calculation
    # Penalties: Critical (-20), High Risk (-10), Ambiguous (-5)
    penalty = (critical_violations * 20) + (high_risk_violations * 10) + (ambiguous_assets * 5)
    readiness_score = max(0, 100 - penalty)
    
    sovereignty_status = "❌ FAIL (Regional Drift)" if "drift detected" in findings_str.lower() else "✅ PASS"

    # 3. BUILD THE TRUTHFUL EXECUTIVE SUMMARY
    executive_summary = f"""# 🛡️ AIGovern Warden: Executive Audit Report
**Date:** {timestamp}
**Target Subscription:** `{sub_id}`
**Framework:** EU AI Act (August 2026 Readiness)

---

## 📊 Executive Compliance Scorecard
| Metric | Status |
| :--- | :--- |
| **Total Assets Analyzed** | {total_assets} |
| **Critical Violations (Signal 9-10)** | {critical_violations} |
| **High-Risk/Drift (Signal 7-8)** | {high_risk_violations} |
| **Readiness Score** | **{readiness_score}%** |

> **Architect's Note:** This score is derived via deterministic extraction. 
> A score of **{readiness_score}%** reflects **{critical_violations + high_risk_violations}** assets requiring immediate intervention.

---
"""

    # 4. FINAL CLEANUP: Convert findings back to readable Markdown
    # We strip the list brackets and quotes for the final file
    clean_findings = findings_str.strip("[]").replace("\\n", "\n").replace("', '", "\n\n")
    
    full_report = executive_summary + "## 🔍 Detailed Audit Findings\n" + clean_findings
    
    with open("warden_executive_audit.md", "w", encoding="utf-8") as f:
        f.write(full_report)
        
    return {"findings": state["findings"]}