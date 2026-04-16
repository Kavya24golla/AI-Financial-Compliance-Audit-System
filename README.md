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
- Offers a human-readable React dashboard backed by a FastAPI service

## How to run
```bash
pip install -r requirements.txt
uvicorn api.app:app --reload
cd frontend
npm install
npm run dev
```

Backend runs on `http://127.0.0.1:8000`.
Frontend runs on `http://127.0.0.1:5173`.

## Website experience
- Choose a company from a simple dropdown
- Run the compliance review
- Read a plain-English summary of the result
- See key financial metrics, issues, anomalies, and the agent timeline without raw JSON overload

## Default demo data
SEC filing caches and knowledge-base assets are already included for demo use.

## Evaluation fit
This project emphasizes:
- domain depth through finance-specific rules and workflows
- compliance guardrails through a rule engine
- edge-case handling through anomaly flags and approval routing
- full task completion through an end-to-end pipeline
- auditability through structured logs and reasoning traces
