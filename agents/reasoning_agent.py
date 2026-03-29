import json
from datetime import datetime
from pathlib import Path

class ReasoningAgent:
    def __init__(self, log_path="memory/reasoning_logs.json"):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.log_path.exists():
            self.log_path.write_text("[]", encoding="utf-8")

    def log_reasoning(self, data):
        compliance = data.get("compliance", {})
        decision = data.get("decision", {})
        financials = data.get("financials", {})
        ratios = financials.get("Ratios", {})

        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "risk_level": compliance.get("risk_level"),
            "risk_score": compliance.get("risk_score"),
            "confidence": compliance.get("confidence"),
            "decision": decision.get("decision"),
            "reason": compliance.get("recommendation"),
            "rules_triggered": [r.get("rule_id") for r in compliance.get("rule_hits", [])],
            "ratios": ratios,
            "issues": compliance.get("compliance_issues", [])
        }

        existing = json.loads(self.log_path.read_text(encoding="utf-8"))
        existing.append(entry)
        self.log_path.write_text(json.dumps(existing, indent=2), encoding="utf-8")
        return entry