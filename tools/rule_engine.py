class RuleEngine:
    def apply_rules(self, recon_data):
        print("\nApplying compliance rules...")

        anomalies = recon_data.get("anomalies", [])
        flags = recon_data.get("reconciliation_flags", [])
        ratios = recon_data.get("financials", {}).get("Ratios", {})

        compliance_issues = []
        rule_hits = []
        risk_score = 0

        # Reconciliation
        if flags:
            compliance_issues.append("Reconciliation mismatch detected")
            risk_score += 25

        # Ratio rules
        if ratios.get("debt_to_asset") and ratios["debt_to_asset"] > 0.9:
            compliance_issues.append("Debt ratio extremely high")
            risk_score += 40

        if ratios.get("cash_ratio") and ratios["cash_ratio"] < 0.02:
            compliance_issues.append("Cash ratio extremely low")
            risk_score += 40

        if ratios.get("expense_to_revenue") and ratios["expense_to_revenue"] > 0.85:
            compliance_issues.append("Expense ratio extremely high")
            risk_score += 40

        if ratios.get("net_margin") and ratios["net_margin"] > 0.6:
            compliance_issues.append("Unusually high profit margin")
            risk_score += 20

        if ratios.get("return_on_assets") and ratios["return_on_assets"] > 0.35:
            compliance_issues.append("Return on assets unusually high")
            risk_score += 20

        if ratios.get("current_ratio") and ratios["current_ratio"] < 1:
            compliance_issues.append("Liquidity risk: Current ratio low")
            risk_score += 20

        if ratios.get("asset_turnover") and ratios["asset_turnover"] < 0.2:
            compliance_issues.append("Low asset turnover")
            risk_score += 15

        if ratios.get("profit_to_expense") and ratios["profit_to_expense"] > 2:
            compliance_issues.append("Profit unusually high vs expenses")
            risk_score += 20

        # Anomalies
        if anomalies:
            compliance_issues.append("Financial anomalies detected")
            risk_score += 15

        # Risk level
        if risk_score >= 70:
            risk_level = "High"
        elif risk_score >= 30:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        # Recommendation
        if risk_level == "High":
            recommendation = "Escalate to finance lead immediately"
        elif risk_level == "Medium":
            recommendation = "Manual review recommended before approval"
        else:
            recommendation = "Auto-approve with audit log entry"

        confidence = min(0.99, round(risk_score / 100, 2))

        return {
            "compliance_issues": compliance_issues,
            "risk_score": risk_score,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "confidence": confidence
        }