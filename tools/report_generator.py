from __future__ import annotations
from pathlib import Path
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

class ReportGenerator:
    def generate_pdf(self, df: pd.DataFrame, summary: dict, output_path: str) -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        doc = SimpleDocTemplate(str(path), pagesize=A4)
        styles = getSampleStyleSheet()
        story = []

        story.append(Paragraph("Socratic-Ledger Compliance Report", styles["Title"]))
        story.append(Spacer(1, 12))
        story.append(Paragraph(f"Decision summary: {summary.get('decision_summary', 'N/A')}", styles["BodyText"]))
        story.append(Paragraph(f"Total rows: {summary.get('total_rows', 0)}", styles["BodyText"]))
        story.append(Paragraph(f"High risk items: {summary.get('high_risk', 0)}", styles["BodyText"]))
        story.append(Spacer(1, 12))

        table_data = [["transaction_id", "vendor", "amount", "risk_score", "risk_level", "decision"]]
        for _, row in df.head(20).iterrows():
            table_data.append([
                str(row.get("transaction_id", "")),
                str(row.get("vendor", "")),
                f"{float(row.get('amount', 0)):.2f}",
                str(int(row.get("risk_score", 0))),
                str(row.get("risk_level", "")),
                str(row.get("decision", "")),
            ])

        table = Table(table_data, repeatRows=1)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story.append(table)
        doc.build(story)
        return str(path)
