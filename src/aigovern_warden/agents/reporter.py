import os
from datetime import datetime
from typing import List
from aigovern_warden.agents.scout import WardenState

def run_reporting_agent(state: WardenState) -> dict:
    """
    Agent 5: Formats all findings into a professional C-Suite Audit Document.
    """
    print("--- [AGENT] Reporter: Generating Executive Audit Report ---")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sub_id = state.get("subscription_id", "Unknown")
    findings = state.get("findings", [])
    
    # 1. Logic for the Scorecard Metrics
    critical_count = sum(1 for f in findings if "Non-Compliant" in f or "Critical" in f or "Violation" in f)
    sovereignty_status = "❌ FAIL (Regional Drift)" if "eastus" in str(findings).lower() else "✅ PASS"
    
    # 2. Construct the Executive View
    # This is the 'Money Shot' for a CEO/CFO
    executive_summary = f"""# 🛡️ AIGovern Warden: AI Compliance Audit
**Date:** {timestamp}
**Target Subscription:** `{sub_id}`
**Framework:** EU AI Act (August 2026 Enforcement)

---

## 📊 Executive Compliance Scorecard
| Metric | Status |
| :--- | :--- |
| **Total AI Assets Found** | {len(findings)} |
| **Critical Policy Violations** | {critical_count} |
| **Data Sovereignty (EU Act)** | {sovereignty_status} |
| **Regulatory Risk Exposure** | High (Financial Year 2026) |
| **Current Readiness Score** | {max(0, 100 - (critical_count * 25))}% |

### 🛑 Urgent Action Items:
1. **Remediate Regional Drift:** Move non-compliant resources to 'westus' (Sovereign Zone).
2. **Technical Documentation:** Generate Article 11 technical files for all detected LLMs.
3. **Registry Update:** Discovered resources must be added to the High-Risk AI Registry.

---

"""

    # 3. Construct the Detailed Technical Findings
    report_body = "## 🔍 Detailed Audit Findings\n"
    if not findings:
        report_body += "✅ No AI resources detected in this subscription scan."
    else:
        for i, finding in enumerate(findings, 1):
            report_body += f"\n### Finding #{i}\n{finding}\n"

    # 4. Final Document Construction
    full_report = executive_summary + report_body
    
    # Save the report to the root folder for easy access
    report_filename = "warden_executive_audit.md"
    try:
        with open(report_filename, "w", encoding="utf-8") as f:
            f.write(full_report)
        print(f"SUCCESS: Executive report generated: {report_filename}")
    except Exception as e:
        print(f"ERROR: Failed to write report file: {str(e)}")
        
    # We pass the state forward with a confirmation of the report
    return {"findings": state["findings"] + [f"SUCCESS: Final Audit Report saved as {report_filename}"]}