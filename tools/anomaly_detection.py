class AnomalyDetectionTool:
    def detect_anomalies(self, financials):
        anomalies = []
        ratios = financials.get("Ratios", {})

        if ratios.get("net_margin") and ratios["net_margin"] > 0.5:
            anomalies.append({
                "anomaly_id": "A001",
                "title": "Net margin unusually high",
                "severity": "medium",
                "evidence": ratios["net_margin"]
            })

        if ratios.get("debt_to_asset") and ratios["debt_to_asset"] > 0.85:
            anomalies.append({
                "anomaly_id": "A002",
                "title": "Debt ratio very high",
                "severity": "high",
                "evidence": ratios["debt_to_asset"]
            })

        if ratios.get("cash_ratio") and ratios["cash_ratio"] < 0.05:
            anomalies.append({
                "anomaly_id": "A003",
                "title": "Cash ratio very low",
                "severity": "medium",
                "evidence": ratios["cash_ratio"]
            })

        if ratios.get("expense_to_revenue") and ratios["expense_to_revenue"] > 0.8:
            anomalies.append({
                "anomaly_id": "A004",
                "title": "Expenses unusually high",
                "severity": "high",
                "evidence": ratios["expense_to_revenue"]
            })

        if ratios.get("return_on_assets") and ratios["return_on_assets"] > 0.3:
            anomalies.append({
                "anomaly_id": "A005",
                "title": "Return on assets unusually high",
                "severity": "medium",
                "evidence": ratios["return_on_assets"]
            })

        return anomalies