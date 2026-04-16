import { useEffect, useMemo, useState } from "react";

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "");

const METRIC_CONFIG = [
  { label: "Revenue", source: "financialSnapshot", match: "Revenue" },
  { label: "Net income", source: "financialSnapshot", match: "Net Income" },
  { label: "Net margin", source: "ratioSnapshot", match: "Net Margin" },
  { label: "Debt / asset", source: "ratioSnapshot", match: "Debt to Asset" },
  { label: "Cash ratio", source: "ratioSnapshot", match: "Cash Ratio" },
  { label: "Expense / revenue", source: "ratioSnapshot", match: "Expense to Revenue" },
];

function MetricCard({ label, value }) {
  return (
    <article className="metric-card">
      <span>{label}</span>
      <strong>{value}</strong>
    </article>
  );
}

function trimCopy(text, maxLength = 180) {
  if (!text) {
    return "";
  }

  return text.length > maxLength ? `${text.slice(0, maxLength).trim()}...` : text;
}

function formatTimestamp(value) {
  if (!value) {
    return "Not available";
  }

  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) {
    return value;
  }

  return new Intl.DateTimeFormat("en-IN", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(parsed);
}

function getMetricValue(result, config) {
  const collection = result?.[config.source] || [];
  const match = collection.find((item) => item.label === config.match);
  return match?.value || "Not available";
}

function getTopReasons(result) {
  const reasons = [
    ...(result?.issues || []),
    ...((result?.anomalies || []).map((item) => item.title) || []),
  ];

  return [...new Set(reasons)].slice(0, 3);
}

function App() {
  const [companies, setCompanies] = useState([]);
  const [selectedCompany, setSelectedCompany] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [loadingCompanies, setLoadingCompanies] = useState(true);
  const [error, setError] = useState("");
  const [artifactTab, setArtifactTab] = useState("report");

  useEffect(() => {
    async function loadCompanies() {
      setLoadingCompanies(true);

      try {
        const response = await fetch(`${API_BASE}/api/companies`);
        if (!response.ok) {
          throw new Error("Could not load companies.");
        }

        const payload = await response.json();
        setCompanies(payload.companies || []);

        if (payload.companies?.length) {
          setSelectedCompany(payload.companies[0].name);
        }
      } catch (loadError) {
        setError(loadError.message);
      } finally {
        setLoadingCompanies(false);
      }
    }

    loadCompanies();
  }, []);

  async function handleAnalyze(event) {
    event.preventDefault();
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_BASE}/api/analyze`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ company: selectedCompany }),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload.detail || "Analysis failed.");
      }

      setResult(payload);
      setArtifactTab("report");
    } catch (analysisError) {
      setError(analysisError.message);
      setResult(null);
    } finally {
      setLoading(false);
    }
  }

  const riskTone = result?.overview?.riskLevel?.toLowerCase() || "neutral";
  const topReasons = useMemo(() => getTopReasons(result), [result]);
  const reportPreview = trimCopy(result?.report?.text, 220);

  return (
    <div className="app-shell">
      <div className="mesh mesh-one" />
      <div className="mesh mesh-two" />

      <div className="container">
        <header className="topbar">
          <div>
            <p className="kicker">Socratic Ledger</p>
            <h1>AI compliance review, built for decisions.</h1>
            <p className="subcopy">
              Run a live review on SEC-backed company data and surface the risk,
              reasons, and next action in one screen.
            </p>
          </div>

          <form onSubmit={handleAnalyze} className="hero-actions">
            <label htmlFor="company">Company</label>
            <div className="hero-controls">
              <select
                id="company"
                value={selectedCompany}
                onChange={(event) => setSelectedCompany(event.target.value)}
                disabled={loadingCompanies || loading}
              >
                {companies.map((company) => (
                  <option key={company.cik} value={company.name}>
                    {company.name}
                  </option>
                ))}
              </select>

              <button
                type="submit"
                disabled={!selectedCompany || loading || loadingCompanies}
              >
                {loading ? "Running..." : "Run review"}
              </button>
            </div>
            {error ? <p className="inline-error">{error}</p> : null}
          </form>
        </header>

        {result ? (
          <main className="dashboard">
            <section className={`decision-card tone-${riskTone}`}>
              <div className="decision-main">
                <div className="decision-head">
                  <div>
                    <p className="kicker">Latest review</p>
                    <h2>{result.company.name}</h2>
                  </div>
                  <span className={`risk-pill ${riskTone}`}>
                    {result.overview.riskLevel} Risk
                  </span>
                </div>

                <div className="decision-grid">
                  <div className="decision-copy">
                    <div className="decision-label">Decision</div>
                    <div className="decision-value">{result.overview.decision}</div>
                    <p className="decision-summary">{trimCopy(result.overview.summary, 150)}</p>

                    <div className="content-block">
                      <div className="block-label">Why flagged</div>
                      <ul className="reason-list">
                        {topReasons.length ? (
                          topReasons.map((reason) => <li key={reason}>{reason}</li>)
                        ) : (
                          <li>No flagged reasons returned.</li>
                        )}
                      </ul>
                    </div>

                    <div className="content-block">
                      <div className="block-label">Next step</div>
                      <p className="next-step">{result.overview.nextStep}</p>
                    </div>
                  </div>

                  <aside className="decision-side">
                    <div className="side-stat">
                      <span>Risk score</span>
                      <strong>{result.overview.riskScore}</strong>
                    </div>
                    <div className="side-stat">
                      <span>Confidence</span>
                      <strong>{result.overview.confidencePercent}%</strong>
                    </div>
                    <div className="side-stat">
                      <span>Company CIK</span>
                      <strong>{result.company.cik}</strong>
                    </div>
                  </aside>
                </div>
              </div>
            </section>

            <section className="surface-card">
              <div className="section-topline">
                <div>
                  <p className="kicker">Key metrics</p>
                  <h3>Financial snapshot</h3>
                </div>
              </div>

              <div className="metrics-grid">
                {METRIC_CONFIG.map((metric) => (
                  <MetricCard
                    key={metric.label}
                    label={metric.label}
                    value={getMetricValue(result, metric)}
                  />
                ))}
              </div>
            </section>

            <section className="lower-grid">
              <details className="fold-card" open>
                <summary>
                  <span>Reasoning trace</span>
                  <small>{result.timeline.length} steps</small>
                </summary>

                <ol className="trace-list">
                  {result.timeline.map((step, index) => (
                    <li key={`${step.agent}-${index}`}>
                      <strong>{step.agent}</strong>
                      <span>{step.status}</span>
                    </li>
                  ))}
                </ol>
              </details>

              <section className="surface-card artifact-card">
                <div className="section-topline artifact-topline">
                  <div>
                    <p className="kicker">Outputs</p>
                    <h3>Report and audit</h3>
                  </div>

                  <div className="tab-switch">
                    <button
                      type="button"
                      className={artifactTab === "report" ? "active" : ""}
                      onClick={() => setArtifactTab("report")}
                    >
                      Report
                    </button>
                    <button
                      type="button"
                      className={artifactTab === "audit" ? "active" : ""}
                      onClick={() => setArtifactTab("audit")}
                    >
                      Audit
                    </button>
                  </div>
                </div>

                {artifactTab === "report" ? (
                  <div className="artifact-panel">
                    <p className="artifact-preview">{reportPreview || "No report available."}</p>
                    <details className="report-fold">
                      <summary>Open full report</summary>
                      <div className="report-body">{result.report.text}</div>
                    </details>
                  </div>
                ) : (
                  <div className="artifact-panel audit-grid">
                    <div className="audit-tile">
                      <span>Timestamp</span>
                      <strong>{formatTimestamp(result.latestAudit?.timestamp)}</strong>
                    </div>
                    <div className="audit-tile">
                      <span>Decision</span>
                      <strong>{result.latestAudit?.decision || result.overview.decision}</strong>
                    </div>
                    <div className="audit-tile">
                      <span>Risk score</span>
                      <strong>{result.latestAudit?.risk_score || result.overview.riskScore}</strong>
                    </div>
                    <div className="audit-tile">
                      <span>Issues logged</span>
                      <strong>{result.latestAudit?.issues?.length || result.issues.length}</strong>
                    </div>
                  </div>
                )}
              </section>
            </section>
          </main>
        ) : (
          <main className="dashboard">
            <section className="empty-card">
              <p className="kicker">Ready</p>
              <h2>No review running yet.</h2>
              <p>Select a company and run the review to load the decision workspace.</p>
            </section>
          </main>
        )}
      </div>
    </div>
  );
}

export default App;
