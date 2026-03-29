class DecisionAgent:
    def decide(self, data):
        print("\nMaking decision based on compliance risk...")

        compliance = data.get("compliance", {})
        risk_level = compliance.get("risk_level")
        confidence = compliance.get("confidence", 0)

        if risk_level == "High":
            decision = "Escalate"
            action = "Send to senior finance officer for investigation"
        elif risk_level == "Medium":
            decision = "Review"
            action = "Manual review required before approval"
        else:
            decision = "Approve"
            action = "Auto-approved with audit logging"

        data["decision"] = {
            "decision": decision,
            "action": action,
            "confidence": confidence
        }

        print("Decision:", decision)
        print("Action:", action)
        print("Confidence:", confidence)

        return data