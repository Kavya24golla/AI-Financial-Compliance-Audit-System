class XBRLParser:
    def extract_financials(self, company_facts):
        facts = company_facts.get("facts", {})
        us_gaap = facts.get("us-gaap", {})

        financials = {}

        def get_value_from_tags(tag_list):
            for tag in tag_list:
                try:
                    if tag in us_gaap:
                        units = us_gaap[tag]["units"]
                        unit_key = list(units.keys())[0]
                        values = units[unit_key]
                        # Get latest non-null value
                        for item in reversed(values):
                            if "val" in item:
                                return item["val"]
                except:
                    continue
            return None

        # Try multiple tags for each financial metric
        financials["Revenue"] = get_value_from_tags([
            "Revenues",
            "SalesRevenueNet",
            "RevenueFromContractWithCustomerExcludingAssessedTax"
        ])

        financials["NetIncome"] = get_value_from_tags([
            "NetIncomeLoss"
        ])

        financials["Assets"] = get_value_from_tags([
            "Assets"
        ])

        financials["Liabilities"] = get_value_from_tags([
            "Liabilities",
            "LiabilitiesAndStockholdersEquity"
        ])

        financials["Cash"] = get_value_from_tags([
            "CashAndCashEquivalentsAtCarryingValue",
            "CashCashEquivalentsRestrictedCashAndRestrictedCashEquivalents"
        ])

        financials["OperatingExpenses"] = get_value_from_tags([
            "OperatingExpenses",
            "CostsAndExpenses"
        ])

        # Compute ratios safely
        revenue = financials.get("Revenue") or 0
        net_income = financials.get("NetIncome") or 0
        assets = financials.get("Assets") or 0
        liabilities = financials.get("Liabilities") or 0
        cash = financials.get("Cash") or 0
        expenses = financials.get("OperatingExpenses") or 0

        financials["Ratios"] = {
            "net_margin": round(net_income / revenue, 4) if revenue else None,
            "debt_to_asset": round(liabilities / assets, 4) if assets else None,
            "cash_to_assets": round(cash / assets, 4) if assets else None,
            "expense_to_revenue": round(expenses / revenue, 4) if revenue else None,
            "return_on_assets": round(net_income / assets, 4) if assets else None,
            "liability_ratio": round(liabilities / assets, 4) if assets else None,
            "cash_ratio": round(cash / liabilities, 4) if liabilities else None,
            "current_ratio": round(assets / liabilities, 4) if liabilities else None,
            "asset_turnover": round(revenue / assets, 4) if assets else None,
            "profit_to_expense": round(net_income / expenses, 4) if expenses else None
        }

        return financials