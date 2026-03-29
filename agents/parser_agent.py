from tools.xbrl_parser import XBRLParser

class ParserAgent:
    def __init__(self):
        self.parser = XBRLParser()

    def parse_financial_data(self, edgar_data):
        print("Parsing financial statements...")
        company_facts = edgar_data["facts"]
        financials = self.parser.extract_financials(company_facts)

        print("Extracted Financial Metrics:")
        for k, v in financials.items():
            if k != "Ratios":
                print(k, ":", v)

        print("Extracted Ratios:")
        for k, v in financials.get("Ratios", {}).items():
            print(k, ":", v)

        return financials