class ReconciliationAgent:
    def reconcile(self, financials):
        print("\nRunning financial reconciliation...")

        results = {}
        flags = []

        revenue = financials.get("Revenue")
        net_income = financials.get("NetIncome")
        expenses = financials.get("OperatingExpenses")
        assets = financials.get("Assets")
        liabilities = financials.get("Liabilities")

        # Revenue vs Expenses check
        if revenue and expenses and net_income:
            calc_income = revenue - expenses
            diff = abs(calc_income - net_income)

            results["IncomeCheckDifference"] = diff

            if diff > revenue * 0.1:
                flags.append("Income mismatch between revenue, expenses, and net income")

        # Assets vs Liabilities check
        if assets and liabilities:
            if liabilities > assets:
                flags.append("Liabilities exceed assets")

        # Cash ratio check
        cash = financials.get("Cash")
        if cash and assets:
            ratio = cash / assets
            results["CashAssetRatio"] = ratio

            if ratio < 0.01:
                flags.append("Very low cash compared to assets")

        print("Reconciliation Results:", results)
        print("Reconciliation Flags:", flags)

        return {
            "financials": financials,
            "reconciliation_results": results,
            "reconciliation_flags": flags
        }