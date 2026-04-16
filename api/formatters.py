from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


def _extract_json_blob(raw_text: str) -> dict[str, Any]:
    if not raw_text:
        return {}

    match = re.search(r"\{.*\}", raw_text, re.DOTALL)
    if not match:
        return {}

    try:
        return json.loads(match.group(0))
    except json.JSONDecodeError:
        return {}


def _format_money(value: Any) -> str:
    if value in (None, ""):
        return "Not available"

    try:
        amount = float(value)
    except (TypeError, ValueError):
        return str(value)

    abs_amount = abs(amount)
    if abs_amount >= 1_000_000_000:
        return f"${amount / 1_000_000_000:.1f}B"
    if abs_amount >= 1_000_000:
        return f"${amount / 1_000_000:.1f}M"
    if abs_amount >= 1_000:
        return f"${amount / 1_000:.1f}K"
    return f"${amount:,.0f}"


def _format_percent(value: Any) -> str:
    if value in (None, ""):
        return "Not available"

    try:
        return f"{float(value) * 100:.1f}%"
    except (TypeError, ValueError):
        return str(value)


def _latest_audit_entry(log_path: str = "memory/audit_log.json") -> dict[str, Any] | None:
    path = Path(log_path)
    if not path.exists():
        return None

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None

    if not payload:
        return None

    return payload[-1]


def _simple_summary(company_name: str, risk_level: str, issues: list[str], decision: str) -> str:
    if issues:
        leading_issue = issues[0]
        return (
            f"{company_name} was marked as {risk_level.lower()} risk and the system recommends "
            f"'{decision}'. The strongest reason was: {leading_issue}."
        )

    return (
        f"{company_name} was marked as {risk_level.lower()} risk and the system recommends "
        f"'{decision}'. No major compliance issue text was returned, so a human review is still advised."
    )


def build_analysis_response(company_name: str, cik: str, raw_result: dict[str, Any]) -> dict[str, Any]:
    financials = raw_result.get("financials", {})
    ratios = financials.get("Ratios", {})
    anomalies = raw_result.get("anomalies") or []
    compliance = raw_result.get("compliance") or {}
    decision = raw_result.get("decision") or {}
    report = raw_result.get("report") or {}
    reasoning_entry = raw_result.get("llm_explanation") or {}
    parsed_reasoning = _extract_json_blob(reasoning_entry.get("explanation_raw", ""))
    issues = compliance.get("compliance_issues") or []
    latest_audit = _latest_audit_entry()

    confidence = decision.get("confidence")
    if confidence is None:
        confidence = compliance.get("confidence", 0)

    risk_level = compliance.get("risk_level", "Unknown")
    decision_label = decision.get("decision", "Review")

    financial_snapshot = [
        {"label": "Revenue", "value": _format_money(financials.get("Revenue"))},
        {"label": "Net Income", "value": _format_money(financials.get("NetIncome"))},
        {"label": "Assets", "value": _format_money(financials.get("Assets"))},
        {"label": "Liabilities", "value": _format_money(financials.get("Liabilities"))},
        {"label": "Cash", "value": _format_money(financials.get("Cash"))},
        {"label": "Operating Expenses", "value": _format_money(financials.get("OperatingExpenses"))},
    ]

    ratio_snapshot = [
        {"label": "Net Margin", "value": _format_percent(ratios.get("net_margin"))},
        {"label": "Debt to Asset", "value": _format_percent(ratios.get("debt_to_asset"))},
        {"label": "Cash Ratio", "value": _format_percent(ratios.get("cash_ratio"))},
        {"label": "Expense to Revenue", "value": _format_percent(ratios.get("expense_to_revenue"))},
        {"label": "Return on Assets", "value": _format_percent(ratios.get("return_on_assets"))},
    ]

    plain_summary = parsed_reasoning.get("explanation") or _simple_summary(
        company_name, risk_level, issues, decision_label
    )

    next_step = (
        parsed_reasoning.get("recommended_next_step")
        or decision.get("action")
        or compliance.get("recommendation")
        or "Manual review is recommended."
    )

    why_flagged = parsed_reasoning.get("why_flagged")
    if not why_flagged:
        why_flagged = "No extra narrative was returned. Review the listed compliance issues for context."

    return {
        "company": {"name": company_name, "cik": cik},
        "overview": {
            "headline": f"{company_name} compliance review finished",
            "riskLevel": risk_level,
            "riskScore": compliance.get("risk_score", "Not available"),
            "decision": decision_label,
            "confidencePercent": round(float(confidence) * 100),
            "summary": plain_summary,
            "nextStep": next_step,
            "whyFlagged": why_flagged,
        },
        "financialSnapshot": financial_snapshot,
        "ratioSnapshot": ratio_snapshot,
        "anomalies": anomalies,
        "issues": issues,
        "recommendation": compliance.get("recommendation"),
        "report": {
            "text": report.get("report_text", "No report text was generated."),
            "savedTo": report.get("saved_to"),
        },
        "timeline": raw_result.get("agent_trace") or [],
        "contextSources": [
            {
                "source": item.get("source", "Unknown"),
                "score": item.get("score", 0),
                "excerpt": (item.get("text", "") or "").strip()[:180],
            }
            for item in (raw_result.get("retrieved_context") or [])
        ],
        "latestAudit": latest_audit,
    }

