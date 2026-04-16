from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from api.formatters import build_analysis_response
from orchestration.pipeline import Pipeline


load_dotenv()

app = FastAPI(
    title="Socratic Ledger API",
    version="2.0.0",
    description="Human-friendly API for financial compliance analysis.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalysisRequest(BaseModel):
    company: str | None = None
    cik: str | None = None


def _load_company_map() -> dict[str, str]:
    company_map_path = Path("data/company_cik_map.json")
    return json.loads(company_map_path.read_text(encoding="utf-8"))


def _friendly_error_message(exc: Exception) -> str:
    message = str(exc)

    if "GROQ_API_KEY" in message:
        return "The AI explanation service is not configured yet. Add GROQ_API_KEY to your environment."
    if "SEC User-Agent" in message or "User-Agent" in message:
        return "The SEC data source is not configured yet. Add SEC_USER_AGENT to your environment."
    if "ProxyError" in message or "Connection" in message or "Max retries exceeded" in message:
        return "The app could not reach the external data services. Please check your network or proxy settings."

    return f"The analysis could not be completed: {message}"


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/companies")
def companies() -> dict[str, list[dict[str, str]]]:
    company_map = _load_company_map()
    return {
        "companies": [
            {"name": name, "cik": cik}
            for name, cik in sorted(company_map.items(), key=lambda item: item[0])
        ]
    }


@app.post("/api/analyze")
def analyze(request: AnalysisRequest) -> dict:
    company_map = _load_company_map()

    cik = request.cik
    company_name = request.company

    if company_name and not cik:
        cik = company_map.get(company_name)
    elif cik and not company_name:
        company_name = next((name for name, value in company_map.items() if value == cik), None)

    if not cik or not company_name:
        raise HTTPException(
            status_code=400,
            detail="Please send a valid company name from the list or a valid CIK.",
        )

    try:
        result = Pipeline().run(
            cik=cik,
            sec_user_agent=os.getenv("SEC_USER_AGENT"),
        )
    except Exception as exc:  # pragma: no cover - runtime guard for external services
        raise HTTPException(status_code=502, detail=_friendly_error_message(exc)) from exc

    return build_analysis_response(company_name, cik, result)

