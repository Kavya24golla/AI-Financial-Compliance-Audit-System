from __future__ import annotations
import pandas as pd

class RiskScorer:
    def score(self, df: pd.DataFrame) -> pd.DataFrame:
        out = df.copy()
        scores = []

        for _, row in out.iterrows():
            score = int(row.get("anomaly_score", 0))
            score += int(row.get("rule_risk_points", 0))

            if bool(row.get("duplicate_invoice", False)):
                score += 20
            if bool(row.get("amount_outlier", False)):
                score += 15
            if str(row.get("vendor", "")).strip() in {"Unknown Corp", "Fake Corp", "Shell Vendor"}:
                score += 25
            if float(row.get("amount", 0)) > 100000:
                score += 25

            scores.append(score)

        out["risk_score"] = scores
        out["risk_level"] = out["risk_score"].apply(lambda x: "High" if x >= 60 else ("Medium" if x >= 30 else "Low"))
        return out
