import streamlit as st
import os
import re

# Set Page Config
st.set_page_config(page_title="AIGovern Warden | Executive Dashboard", layout="wide")

def load_audit_report():
    report_path = "warden_executive_audit.md"
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            return f.read()
    return None

def main():
    st.title("🛡️ AIGovern Warden: AI Compliance Portal")
    st.sidebar.image("https://via.placeholder.com/150?text=WARDEN+AI", width=150)
    st.sidebar.markdown("### 2026 EU AI Act Readiness")
    st.sidebar.info("Monitoring Subscription: `1a317aed-2ae0-467e-a97d-46ea4e51f919`")

    report_content = load_audit_report()

    if not report_content:
        st.warning("No audit report found. Please run the Warden Engine first.")
        if st.button("🚀 Run Warden Scan Now"):
            st.info("Scanning Azure Environment...")
            # Here we would trigger main.py logic
    else:
        # 1. Executive Metrics (Extracted via Regex for Demo)
        st.subheader("📊 High-Level Risk Assessment")
        col1, col2, col3 = st.columns(3)
        
        # Simple parser logic for the dashboard
        readiness_score = re.search(r"Readiness Score\*\* \| (\d+)%", report_content)
        score = readiness_score.group(1) if readiness_score else "0"
        
        col1.metric("Readiness Score", f"{score}%", delta=f"{int(score)-100}%", delta_color="inverse")
        col2.metric("Critical Violations", "3", delta="Action Required", delta_color="normal")
        col3.metric("Regulatory Deadline", "Aug 2026", help="EU AI Act Enforcement Date")

        st.divider()

        # 2. Tabs for different views
        tab1, tab2, tab3 = st.columns([2, 1, 1])
        
        with tab1:
            st.markdown("### 🔍 Detailed Audit Narrative")
            st.markdown(report_content)

        with tab2:
            st.markdown("### 🛠️ Active Remediation")
            st.success("GitHub PR #102 Created")
            st.code("git checkout fix/regional-drift\nterraform apply", language="bash")
            st.button("View Pull Request on GitHub")

        with tab3:
            st.markdown("### ⚖️ Legal Citations")
            st.error("Article 5: Prohibited Practice")
            st.warning("Article 10: Data Governance")
            st.warning("Article 11: Technical Docs")

if __name__ == "__main__":
    main()