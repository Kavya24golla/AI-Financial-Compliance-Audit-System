from __future__ import annotations

import json
from pathlib import Path

from tools.groq_llm import GroqLLM


class ReportAgent:
    def __init__(self):
        self.llm = GroqLLM()

    def generate_report(self, data, retrieved_context=None):
        financials = data.get("financials", {})
        compliance = data.get("compliance", {})
        decision = data.get("decision", {})

        prompt = f"""
You are writing a finance compliance report for a hackathon demo.

Use this structured data:
Financials: {json.dumps(financials, indent=2)}
Compliance: {json.dumps(compliance, indent=2)}
Decision: {json.dumps(decision, indent=2)}
Retrieved Context: {json.dumps(retrieved_context or [], indent=2)}

Write:
1. executive summary
2. why the case was flagged or approved
3. key ratios
4. recommendation
5. final decision
6. audit note

Keep it concise, professional, and understandable to a finance judge.
"""

        report_text = self.llm.chat(
            system_prompt="You are a professional financial reporting assistant.",
            user_prompt=prompt
        )

        out_dir = Path("reports/generated_reports")
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "llm_report.txt").write_text(report_text, encoding="utf-8")

        return {
            "report_text": report_text,
            "saved_to": str(out_dir / "llm_report.txt")
        }