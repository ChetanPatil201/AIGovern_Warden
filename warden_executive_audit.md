# 🛡️ AIGovern Warden: Executive Audit Report
**Date:** 2026-01-06 14:50:29
**Target Subscription:** `1a317aed-2ae0-467e-a97d-46ea4e51f919`
**Framework:** EU AI Act (August 2026 Readiness)

---

## 📊 Executive Compliance Scorecard
| Metric | Status |
| :--- | :--- |
| **Total Assets Analyzed** | 10 |
| **Critical Violations (Signal 9-10)** | 5 |
| **High-Risk/Drift (Signal 7-8)** | 1 |
| **Readiness Score** | **0%** |

> **Architect's Note:** This score is derived via deterministic extraction. 
> A score of **0%** reflects **6** assets requiring immediate intervention.

---
## 🔍 Detailed Audit Findings
'```json
[
  {
    "Resource": "cp-azureopenai",
    "Signal Strength": 9,
    "Verdict": "Categorical",
    "Legal Citation": "Article 10, Article 11",
    "Reasoning": "Explicit AI service detected with \'DRIFT_DETECTED\'. Strong correlation with Articles 10 and 11, which require data governance and documentation. No systemic risk indicated, but resources lack access control and metadata clarity."
  },
  {
    "Resource": "cp-aoi-fnd-svc",
    "Signal Strength": 9,
    "Verdict": "Categorical",
    "Legal Citation": "Article 10, Article 11",
    "Reasoning": "Explicit AI service with \'DRIFT_DETECTED\'. Suggestive violation of Articles 10 and 11 due to lack of access to deployment metadata and systemic data governance concerns. No explicit systemic risk."
  },
  {
    "Resource": "SDS-LLM",
    "Signal Strength": 9,
    "Verdict": "Categorical",
    "Legal Citation": "Article 10, Article 11",
    "Reasoning": "Explicit AI service directly identified. \'DRIFT_DETECTED\' and absence of metadata strongly suggest violations under Articles 10 and 11 regarding documentation and dataset compliance. No systemic risk indicated."
  },
  {
    "Resource": "AIBOTING",
    "Signal Strength": 9,
    "Verdict": "Categorical",
    "Legal Citation": "Article 10, Article 11",
    "Reasoning": "AI service flagged with \'DRIFT_DETECTED\' status and lacking deployment metadata. Strong correlation with Articles 10 and 11 requiring high-risk AI systems to maintain robust governance and documentation standards."
  },
  {
    "Resource": "CityScan-Public-Biometrics",
    "Signal Strength": 10,
    "Verdict": "Categorical",
    "Legal Citation": "Article 5",
    "Reasoning": "The resource \'CityScan-Public-Biometrics\' indicates biometric AI in public spaces for law enforcement—a practice explicitly banned under Article 5. This constitutes a prohibited AI practice with a systemic breach."
  },
  {
    "Resource": "avdingramfslogixstg",
    "Signal Strength": 4,
    "Verdict": "Potential",
    "Legal Citation": "N/A",
    "Reasoning": "Data storage with public access enabled, suggests potential data governance gaps. Requires further documentation to confirm compliance with Article 10. Signal is weaker due to the generic nature of the asset."
  },
  {
    "Resource": "funcappstoragesom",
    "Signal Strength": 4,
    "Verdict": "Potential",
    "Legal Citation": "N/A",
    "Reasoning": "Publicly accessible data store hints at possible data governance issues but lacks explicit AI indicators. Documentation is necessary to establish compliance with Article 10."
  },
  {
    "Resource": "stgterraformtfstate",
    "Signal Strength": 4,
    "Verdict": "Potential",
    "Legal Citation": "N/A",
    "Reasoning": "Generic public storage asset with suggestive metadata (\'terraform\'). Requires review of associated documentation to determine alignment with Article 10."
  },
  {
    "Resource": "storagedatadiskfatcat",
    "Signal Strength": 4,
    "Verdict": "Potential",
    "Legal Citation": "N/A",
    "Reasoning": "Publicly accessible storage with ambiguous connection to AI operations but indicative of a potential governance gap under Article 10."
  },
  {
    "Resource": "nsg-ai-training-public",
    "Signal Strength": 7,
    "Verdict": "Categorical",
    "Legal Citation": "Article 10",
    "Reasoning": "Network security group allowing public SSH access (port 22) constitutes a potential security risk for AI-related environments. Elevated security gaps conflict with Article 10\'s expectations for governance."
  }
]
``` 


### PROPOSED TERRAFORM FIX:
```hcl
resource "azurerm_cognitive_account" "cp_azureopenai_westus" {
  name                = "cp-azureopenai-westus"
  resource_group_name = "example-resource-group"
  location            = "westus"
  kind                = "OpenAI"
  sku_name            = "S0"

  tags = {
    Environment = "Production"
  }
}
```'