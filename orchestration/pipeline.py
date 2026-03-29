from agents.edgar_agent import EdgarAgent
from agents.parser_agent import ParserAgent
from agents.reconciliation_agent import ReconciliationAgent
from agents.anomaly_agent import AnomalyAgent
from agents.compliance_agent import ComplianceAgent
from agents.decision_agent import DecisionAgent
from agents.report_agent import ReportAgent
from agents.audit_agent import AuditAgent
from agents.rag_agent import RAGAgent
from agents.llm_reasoning_agent import LLMReasoningAgent


class Pipeline:
    def run(self, cik="320193", sec_user_agent=None):
        print("\n===== SOCRATIC LEDGER PIPELINE STARTED =====\n")

        # Initialize agents
        edgar = EdgarAgent(user_agent=sec_user_agent)
        parser = ParserAgent()
        recon = ReconciliationAgent()
        anomaly = AnomalyAgent()
        compliance = ComplianceAgent()
        decision = DecisionAgent()
        report = ReportAgent()
        audit = AuditAgent()
        rag = RAGAgent()
        reasoning = LLMReasoningAgent()

        trace = []

        # Step 1: Fetch EDGAR data
        edgar_data = edgar.fetch_company_data(cik)
        trace.append({"agent": "EdgarAgent", "status": "Fetched SEC financial data"})

        # Step 2: Parse financials
        financials = parser.parse_financial_data(edgar_data)
        trace.append({"agent": "ParserAgent", "status": "Extracted financial statements and ratios"})

        # Step 3: Reconciliation
        recon_data = recon.reconcile(financials)
        trace.append({"agent": "ReconciliationAgent", "status": "Reconciliation checks completed"})

        # Step 4: Anomaly Detection
        anomaly_data = anomaly.detect(recon_data)
        trace.append({"agent": "AnomalyAgent", "status": "Financial anomalies evaluated"})

        # Step 5: Compliance Rules
        compliance_data = compliance.check(anomaly_data)
        trace.append({
            "agent": "ComplianceAgent",
            "status": f"Risk score {compliance_data['compliance']['risk_score']}"
        })

        # Step 6: Decision
        decision_data = decision.decide(compliance_data)
        trace.append({
            "agent": "DecisionAgent",
            "status": decision_data["decision"]["decision"]
        })

        # Step 7: RAG Retrieval
        query = f"Financial compliance risk analysis for company CIK {cik}"
        retrieved = rag.retrieve(query, top_k=5)
        trace.append({"agent": "RAGAgent", "status": "Retrieved compliance policies and past cases"})

        # Step 8: LLM Reasoning
        explanation = reasoning.explain(decision_data, retrieved)
        trace.append({"agent": "LLMReasoningAgent", "status": "Generated explanation using LLM"})

        # Step 9: Report Generation
        report_data = report.generate_report(decision_data, retrieved)
        trace.append({"agent": "ReportAgent", "status": "Compliance report generated"})

        # Step 10: Audit Logging
        audit.log(decision_data, trace)
        trace.append({"agent": "AuditAgent", "status": "Audit log saved"})

        print("\n===== PIPELINE COMPLETED =====")

        return {
            "financials": financials,
            "anomalies": anomaly_data.get("anomalies"),
            "compliance": compliance_data.get("compliance"),
            "decision": decision_data.get("decision"),
            "retrieved_context": retrieved,
            "llm_explanation": explanation,
            "report": report_data,
            "agent_trace": trace
        }