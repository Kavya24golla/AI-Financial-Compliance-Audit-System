import json
import os
from datetime import datetime


class AuditAgent:
    def __init__(self, log_file="memory/audit_log.json"):
        self.log_file = log_file

        if not os.path.exists(self.log_file):
            with open(self.log_file, "w") as f:
                json.dump([], f)

    def log(self, decision_data, trace):
        print("Logging audit trail...")

        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "risk_level": decision_data["compliance"]["risk_level"],
            "risk_score": decision_data["compliance"]["risk_score"],
            "decision": decision_data["decision"]["decision"],
            "issues": decision_data["compliance"]["compliance_issues"],
            "agent_trace": trace
        }

        with open(self.log_file, "r") as f:
            logs = json.load(f)

        logs.append(log_entry)

        with open(self.log_file, "w") as f:
            json.dump(logs, f, indent=4)

        print("Audit log saved.")