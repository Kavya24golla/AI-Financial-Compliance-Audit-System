from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

import requests


class EdgarAPI:
    """
    Lightweight EDGAR client for hackathon use.

    What it does:
    - Fetches SEC company facts
    - Fetches company submissions
    - Extracts recent filing metadata
    - Saves raw responses to disk for caching/audit
    """

    def __init__(self, user_agent: str, cache_dir: str = "data/raw_filings"):
        if not user_agent or "@" not in user_agent:
            raise ValueError(
                "Please pass a proper SEC User-Agent like: 'Your Name your.email@example.com'"
            )

        self.user_agent = user_agent
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.headers = {
            "User-Agent": self.user_agent,
            "Accept-Encoding": "gzip, deflate",
            "Host": "data.sec.gov",
        }

    def _get_json(self, url: str) -> Dict[str, Any]:
        response = requests.get(url, headers=self.headers, timeout=30)
        response.raise_for_status()
        return response.json()

    def get_company_facts(self, cik: str) -> Dict[str, Any]:
        """
        SEC company facts endpoint.
        """
        cik_padded = str(cik).zfill(10)
        url = f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik_padded}.json"
        data = self._get_json(url)
        self._save_json(data, f"companyfacts_{cik_padded}.json")
        return data

    def get_company_submissions(self, cik: str) -> Dict[str, Any]:
        """
        SEC submissions endpoint.
        """
        cik_padded = str(cik).zfill(10)
        url = f"https://data.sec.gov/submissions/CIK{cik_padded}.json"
        data = self._get_json(url)
        self._save_json(data, f"submissions_{cik_padded}.json")
        return data

    def get_recent_filings(self, cik: str, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Returns recent filing metadata from the SEC submissions response.
        """
        submissions = self.get_company_submissions(cik)
        recent = submissions.get("filings", {}).get("recent", {})

        forms = recent.get("form", [])
        accession_numbers = recent.get("accessionNumber", [])
        filing_dates = recent.get("filingDate", [])
        primary_docs = recent.get("primaryDocument", [])
        report_dates = recent.get("reportDate", [])

        filings = []
        for i in range(min(limit, len(forms))):
            filings.append(
                {
                    "cik": str(cik).zfill(10),
                    "form": forms[i] if i < len(forms) else "",
                    "accession_number": accession_numbers[i] if i < len(accession_numbers) else "",
                    "filing_date": filing_dates[i] if i < len(filing_dates) else "",
                    "report_date": report_dates[i] if i < len(report_dates) else "",
                    "primary_document": primary_docs[i] if i < len(primary_docs) else "",
                }
            )

        self._save_json(filings, f"recent_filings_{str(cik).zfill(10)}.json")
        return filings

    def _save_json(self, payload: Any, filename: str) -> None:
        path = self.cache_dir / filename
        path.write_text(json.dumps(payload, indent=2), encoding="utf-8")