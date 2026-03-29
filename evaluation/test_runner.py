import json
import time
import os
from copy import deepcopy
from dotenv import load_dotenv

from agents.reconciliation_agent import ReconciliationAgent
from agents.anomaly_agent import AnomalyAgent
from agents.compliance_agent import ComplianceAgent
from agents.decision_agent import DecisionAgent
from agents.rag_agent import RAGAgent
from agents.llm_reasoning_agent import LLMReasoningAgent
from agents.report_agent import ReportAgent

from evaluation.metrics import evaluate_metrics

load_dotenv()


def add_ratios(financials):
    """Add financial ratios to synthetic test cases"""
    f = deepcopy(financials)

    revenue = f.get("Revenue") or 0
    net_income = f.get("NetIncome") or 0
    assets = f.get("Assets") or 0
    liabilities = f.get("Liabilities") or 0
    cash = f.get("Cash") or 0
    expenses = f.get("OperatingExpenses") or 0

    f["Ratios"] = {
        "net_margin": round(net_income / revenue, 4) if revenue else None,
        "debt_to_asset": round(liabilities / assets, 4) if assets else None,
        "cash_to_assets": round(cash / assets, 4) if assets else None,
        "expense_to_revenue": round(expenses / revenue, 4) if revenue else None,
        "return_on_assets": round(net_income / assets, 4) if assets else None,
        "liability_ratio": round(liabilities / assets, 4) if assets else None,
        "cash_ratio": round(cash / liabilities, 4) if liabilities else None
    }

    return f


def run_tests():
    recon = ReconciliationAgent()
    anomaly = AnomalyAgent()
    compliance = ComplianceAgent()
    decision = DecisionAgent()
    rag = RAGAgent()
    llm = LLMReasoningAgent()
    report = ReportAgent()

    with open("data/test_cases/financial_test_cases.json") as f:
        test_cases = json.load(f)

    results = []
    start_time = time.time()

    for case in test_cases:
        print("\n======================")
        print("Test Case:", case["case"])

        financials = add_ratios(case["financials"])

        recon_data = recon.reconcile(financials)
        anomaly_data = anomaly.detect(recon_data)
        compliance_data = compliance.check(anomaly_data)
        decision_data = decision.decide(compliance_data)

        # RAG Retrieval
        query = f"Financial risk analysis for case {case['case']}"
        retrieved = rag.retrieve(query, top_k=5)

        # LLM Explanation
        explanation = llm.explain(decision_data, retrieved)

        # Report Generation
        report_data = report.generate_report(decision_data, retrieved)

        results.append({
            "case": case["case"],
            "risk_level": decision_data["compliance"]["risk_level"],
            "risk_score": decision_data["compliance"]["risk_score"],
            "decision": decision_data["decision"]["decision"],
            "anomalies": len(anomaly_data.get("anomalies", [])),
            "llm_used": True
        })

        print("Decision:", decision_data["decision"]["decision"])
        print("Risk Level:", decision_data["compliance"]["risk_level"])
        print("LLM Explanation Generated")
        print("Report Saved:", report_data.get("saved_to"))

    end_time = time.time()
    processing_time = end_time - start_time

    print("\n===== SUMMARY =====")
    for r in results:
        print(r)

    evaluate_metrics(results, processing_time)


if __name__ == "__main__":
    run_tests()