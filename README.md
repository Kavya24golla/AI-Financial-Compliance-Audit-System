# AI Financial Compliance & Audit System

**AI Financial Compliance & Audit System** is a multi-agent AI system that analyzes SEC filings, detects financial anomalies, applies compliance rules, assigns risk scores, explains decisions using LLMs, and maintains a full audit trail.
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
=======
---

## Overview

This system automates the financial compliance and audit workflow by processing SEC EDGAR filings, extracting financial statements, calculating ratios, detecting anomalies, applying rule-based compliance checks, and generating explainable decisions using Retrieval Augmented Generation (RAG) and Large Language Models (LLMs).


It simulates a real-world financial compliance environment where analysts review statements, enforce policies, and document decisions.

---

## Problem Statement

Financial compliance and auditing of company financial statements is:

- Time-consuming  
- Expensive  
- Prone to human error  

Analysts must:
- Analyze financial ratios  
- Detect anomalies  
- Validate accounting consistency  
- Apply compliance policies  
- Assign risk scores  
- Explain decisions  
- Maintain audit logs  

This system automates the entire pipeline.

---

## Solution Overview

The system performs:

1. Fetches financial data from SEC EDGAR  
2. Extracts and processes financial statements  
3. Calculates financial ratios  
4. Performs reconciliation checks  
5. Detects anomalies  
6. Applies compliance rules  
7. Assigns risk scores  
8. Generates decisions (**Approve / Review / Escalate**)  
9. Retrieves policies using RAG  
10. Generates LLM-based explanations  
11. Creates compliance reports  
12. Maintains a complete audit trail  
13. Displays results via dashboard  

---

## System Architecture

EDGAR Agent → Parser Agent → Ratio Engine → Reconciliation Agent →  
Anomaly Agent → Compliance Agent → Decision Agent →  
RAG Agent → LLM Reasoning Agent → Report Agent → Audit Agent → UI

---

## Features

- SEC EDGAR data ingestion  
- Financial ratio analysis  
- Reconciliation checks  
- Anomaly detection  
- Rule-based compliance engine  
- Risk scoring system  
- Automated decision engine  
- RAG-based knowledge retrieval  
- LLM-generated explanations  
- Compliance report generation  
- Full audit trail logging  
- Evaluation and testing pipeline  
- Streamlit dashboard  
- Downloadable reports  

---

## Financial Ratios Used

- Net Margin  
- Debt to Asset Ratio  
- Cash Ratio  
- Expense Ratio  
- Return on Assets  
- Current Ratio  
- Asset Turnover  
- Profit to Expense Ratio  

---

## Compliance & Risk Rules

The system detects:

- High debt ratio  
- Low cash ratio  
- Unusual profit margins  
- High expense ratio  
- Low liquidity  
- Reconciliation mismatches  
- Multiple anomalies  

Outputs:

- Risk Score  
- Risk Level (**Low / Medium / High**)  
- Recommendation  
- Final Decision  

---

## Audit Trail

Every step is logged:

- Data extraction  
- Ratio computation  
- Reconciliation results  
- Anomaly detection  
- Rule triggers  
- Risk scoring  
- Decision making  
- Report generation  
- LLM explanations  

---

## Evaluation Focus

- Financial domain expertise  
- Compliance rule enforcement  
- Edge-case handling  
- End-to-end pipeline execution  
- Decision auditability  

---

## Demo Workflow

1. Select company  
2. Run analysis  
3. View financial summary  
4. Check ratios  
5. Review anomalies  
6. See compliance results  
7. Analyze risk score  
8. View final decision  
9. Read AI explanation  
10. Download report  
11. Inspect audit logs  

---

## Technologies Used

- Python  
- SEC EDGAR API  
- Financial Analysis  
- Rule-Based Systems  
- Retrieval Augmented Generation (RAG)  
- Groq LLM API  
- Streamlit  
- JSON Logging  

---

## Project Structure

agents/  
tools/  
orchestration/  
memory/  
evaluation/  
ui/  
data/  
reports/  
main.py  
requirements.txt  
README.md  

---

## How to Run

### Install dependencies  
pip install -r requirements.txt  

### Run application  
streamlit run ui/streamlit_app.py  

---

## Dashboard Outputs

- Financial summary  
- Ratio analysis  
- Anomaly detection  
- Compliance results  
- Risk scoring  
- Final decision  
- AI explanation  
- Downloadable reports  
- Audit logs  

---

## Impact

- Reduces manual audit workload  
- Detects anomalies faster  
- Improves compliance accuracy  
- Provides explainable AI decisions  
- Maintains regulatory audit logs  

---

## Real-World Applications

This system can be used in real-world financial environments such as:

- Corporate financial compliance review  
- Internal and external auditing  
- Banking risk assessment  
- Financial fraud detection  
- Regulatory financial monitoring  
- Investment risk analysis  
- Due diligence automation  
- Accounting anomaly detection  

Financial institutions, auditing firms, and corporate finance teams can use such systems to automate compliance checks and financial risk analysis.

---

## Future Scope

This system can be extended further by:

- Adding fraud detection models  
- Performing financial trend and time-series analysis  
- Integrating regulatory rule databases  
- Adding real-time financial monitoring  
- Multi-company financial comparison  
- Automated compliance alerts  
- Cloud deployment for enterprise usage  
- Advanced financial forecasting  
- Integration with ERP and accounting systems  

---

## Submission Requirements

| Field | Content |
|------|--------|
| Detailed document | PDF |
| Architecture diagram | Image/PDF |
| GitHub URL | Repository link |
| Video link | Google Drive |
| Demo upload | MP4 |

---

## Pitch Line

**AI Financial Compliance & Audit System is a multi-agent AI system that analyzes SEC filings, detects financial anomalies, applies compliance rules, assigns risk scores, explains decisions using LLMs, and maintains a full audit trail.**

---

## Conclusion

This project demonstrates how multi-agent AI can automate financial compliance, risk analysis, decision-making, reporting, and auditing in a single integrated system.
