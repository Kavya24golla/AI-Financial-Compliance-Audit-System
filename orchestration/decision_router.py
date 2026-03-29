from __future__ import annotations

class DecisionRouter:
    def route(self, risk_level: str) -> str:
        if risk_level == "High":
            return "Escalate"
        if risk_level == "Medium":
            return "Review"
        return "Auto-Approve"
