import streamlit as st
import os
import json
from dotenv import load_dotenv
from orchestration.pipeline import Pipeline

load_dotenv()

st.set_page_config(page_title="Socratic Ledger", layout="wide")

st.title("Socratic Ledger - Financial Compliance AI System")

st.markdown("""
This system analyzes SEC financial filings, detects anomalies,
applies compliance rules, assigns risk scores,
and generates AI explanations and audit reports.
""")

# Load company map
with open("data/company_cik_map.json") as f:
    company_map = json.load(f)

company_names = list(company_map.keys())

st.sidebar.header("Company Selection")
selected_company = st.sidebar.selectbox("Select Company", company_names)

run_button = st.sidebar.button("Run Compliance Analysis")

pipeline = Pipeline()

# Use session state to store results
if "result" not in st.session_state:
    st.session_state.result = None

if run_button:
    cik = company_map[selected_company]

    with st.spinner("Running Financial Compliance Pipeline..."):
        result = pipeline.run(
            cik=cik,
            sec_user_agent=os.getenv("SEC_USER_AGENT")
        )

    st.session_state.result = result

# Display results if available
if st.session_state.result:
    result = st.session_state.result

    st.success("Analysis Completed")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Financial Summary")
        st.json(result.get("financials"))

        st.subheader("Financial Ratios")
        if result.get("financials"):
            st.json(result["financials"].get("Ratios"))

    with col2:
        st.subheader("Anomalies Detected")
        st.json(result.get("anomalies"))

        st.subheader("Compliance Results")
        st.json(result.get("compliance"))

    st.subheader("Decision")
    st.json(result.get("decision"))

    st.subheader("LLM Explanation")
    st.write(result.get("llm_explanation"))

    st.subheader("Generated Report")
    report_text = result["report"].get("report_text")
    st.write(report_text)

    # Create full report download
    full_report = {
        "financials": result.get("financials"),
        "anomalies": result.get("anomalies"),
        "compliance": result.get("compliance"),
        "decision": result.get("decision"),
        "llm_explanation": result.get("llm_explanation"),
        "report_text": report_text
    }

    st.download_button(
        label="Download Full Compliance Report",
        data=json.dumps(full_report, indent=4),
        file_name="full_compliance_report.json",
        mime="application/json"
    )

# Audit Logs
st.subheader("Audit Logs")

try:
    with open("memory/audit_log.json", "r") as f:
        logs = json.load(f)
        st.json(logs)

        st.download_button(
            label="Download Audit Logs",
            data=json.dumps(logs, indent=4),
            file_name="audit_logs.json",
            mime="application/json"
        )
except:
    st.write("No audit logs yet.")