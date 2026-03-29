# Socratic-Ledger

An AI financial close and compliance agent built for hackathon Problem Statement 5:
domain expertise, compliance guardrails, edge-case handling, full task completion, and auditable decisions.

## What it does
- Ingests financial transactions and optional filing-like data
- Reconciles transactions
- Detects anomalies and assigns a risk score
- Applies compliance rules
- Produces a decision with reasons
- Writes a complete audit trail
- Generates a report
- Offers a Streamlit dashboard and chat-style report queries

## How to run
```bash
pip install -r requirements.txt
python main.py
streamlit run ui/streamlit_app.py
```

## Default demo data
The app can create a sample dataset automatically if no data is present.

## Evaluation fit
This project emphasizes:
- domain depth through finance-specific rules and workflows
- compliance guardrails through a rule engine
- edge-case handling through anomaly flags and approval routing
- full task completion through an end-to-end pipeline
- auditability through structured logs and reasoning traces
