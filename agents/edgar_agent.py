import os
from dotenv import load_dotenv
from tools.edgar_api import EdgarAPI

load_dotenv()

class EdgarAgent:
    def __init__(self, user_agent=None):
        if user_agent is None:
            user_agent = os.getenv("SEC_USER_AGENT")

        self.api = EdgarAPI(user_agent)

    def fetch_company_data(self, cik):
        print("Fetching EDGAR data...")
        facts = self.api.get_company_facts(cik)
        filings = self.api.get_recent_filings(cik)
        return {"facts": facts, "filings": filings}

    def fetch_company_bundle(self, cik, filing_limit=10):
        print(f"Fetching bundle for CIK {cik}...")
        facts = self.api.get_company_facts(cik)
        filings = self.api.get_recent_filings(cik)

        return {
            "cik": cik,
            "company_facts": facts,
            "recent_filings": filings[:filing_limit]
        }