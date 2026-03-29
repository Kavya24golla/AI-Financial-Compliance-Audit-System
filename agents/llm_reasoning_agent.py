from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

from tools.groq_llm import GroqLLM


class LLMReasoningAgent:
    def __init__(self, log_path: str = "memory/reasoning_logs.json"):
        self.llm = GroqLLM()
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("[]", encoding="utf-8")

    def explain(self, data: dict, retrieved_context: list[dict]) -> dict:
        system_prompt = (
            "You are a senior financial compliance analyst. "
            "Explain decisions clearly, avoid hallucinations, and use only the provided data."
        )

        user_prompt = f"""
Financial Summary:
{json.dumps(data.get("financials", {}), indent=2)}

Ratios:
{json.dumps(data.get("financials", {}).get("Ratios", {}), indent=2)}

Reconciliation:
{json.dumps(data.get("reconciliation_results", {}), indent=2)}

Anomalies:
{json.dumps(data.get("anomalies", []), indent=2)}

Compliance:
{json.dumps(data.get("compliance", {}), indent=2)}

Decision:
{json.dumps(data.get("decision", {}), indent=2)}

Retrieved Context:
{json.dumps(retrieved_context, indent=2)}

Return a short JSON object with:
- explanation
- why_flagged
- recommended_next_step
- confidence_comment
"""

        answer = self.llm.chat(system_prompt, user_prompt)

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "explanation_raw": answer,
            "risk_level": data.get("compliance", {}).get("risk_level"),
            "risk_score": data.get("compliance", {}).get("risk_score"),
            "decision": data.get("decision", {}).get("decision")
        }

        existing = json.loads(self.log_path.read_text(encoding="utf-8"))
        existing.append(entry)
        self.log_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")

        return entry