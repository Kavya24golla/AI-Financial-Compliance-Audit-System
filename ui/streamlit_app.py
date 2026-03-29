from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.express as px

from orchestration.pipeline import Pipeline
from evaluation.metrics import impact_model

st.set_page_config(page_title="Socratic-Ledger", layout="wide")

st.title("Socratic-Ledger")
st.caption("AI Financial Close & Compliance Agent")

if "result" not in st.session_state:
    st.session_state.result = None

with st.sidebar:
    st.header("Actions")
    run = st.button("Run pipeline")
    st.write("Audit trail, compliance, anomaly detection, and report generation are all included.")

if run:
    with st.spinner("Running finance pipeline..."):
        st.session_state.result = Pipeline().run()
        st.success("Pipeline completed.")

result = st.session_state.result

if result:
    df = result["data"]
    summary = result["summary"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Rows", summary["total_rows"])
    c2.metric("High Risk", summary["high_risk"])
    c3.metric("Medium Risk", summary["medium_risk"])
    c4.metric("Low Risk", summary["low_risk"])

    st.subheader("Risk Distribution")
    chart_df = pd.DataFrame({
        "level": ["High", "Medium", "Low"],
        "count": [summary["high_risk"], summary["medium_risk"], summary["low_risk"]]
    })
    st.plotly_chart(px.bar(chart_df, x="level", y="count"), use_container_width=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Transactions", "Reasons", "Audit Log", "Report"])

    with tab1:
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.dataframe(df[["transaction_id", "risk_level", "decision", "reasoning"]], use_container_width=True)

    with tab3:
        audit_path = Path("memory/audit_log.json")
        if audit_path.exists():
            audit = json.loads(audit_path.read_text(encoding="utf-8"))
            st.json(audit)
        else:
            st.info("No audit log yet.")

    with tab4:
        report_path = Path(result["report_path"])
        st.write(f"Report saved to: `{report_path}`")
        if report_path.exists():
            st.success("PDF report generated successfully.")

    st.subheader("Chat with reports")
    prompt = st.text_input("Ask about the report or flagged transactions")
    if prompt:
        prompt_low = prompt.lower()
        if "high risk" in prompt_low:
            st.write(df[df["risk_level"] == "High"][["transaction_id", "vendor", "amount", "risk_score", "decision"]])
        elif "duplicate" in prompt_low:
            st.write(df[df["duplicate_invoice"] == True][["transaction_id", "invoice_id", "vendor", "amount"]])
        elif "why" in prompt_low or "flag" in prompt_low:
            st.write(df[["transaction_id", "reasoning"]])
        else:
            st.write("Try asking: 'show high risk items', 'duplicate invoices', or 'why was this flagged?'")
else:
    st.info("Run the pipeline from the sidebar to view outputs.")

st.divider()
st.subheader("Impact model")
st.json(impact_model())
