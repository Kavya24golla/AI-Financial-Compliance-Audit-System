from tools.rule_engine import RuleEngine

class ComplianceAgent:
    def __init__(self):
        self.engine = RuleEngine()

    def check(self, recon_data):
        print("\nRunning compliance checks...")

        compliance_result = self.engine.apply_rules(recon_data)

        print("Compliance Issues:", compliance_result["compliance_issues"])
        print("Risk Score:", compliance_result["risk_score"])
        print("Risk Level:", compliance_result["risk_level"])
        print("Recommendation:", compliance_result["recommendation"])
        print("Confidence:", compliance_result["confidence"])

        recon_data["compliance"] = compliance_result
        return recon_data