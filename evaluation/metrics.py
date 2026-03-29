def evaluate_metrics(results, processing_time):
    high = medium = low = 0
    approve = review = escalate = 0
    total_risk = 0
    llm_runs = 0

    for r in results:
        if r["risk_level"] == "High":
            high += 1
        elif r["risk_level"] == "Medium":
            medium += 1
        else:
            low += 1

        if r["decision"] == "Approve":
            approve += 1
        elif r["decision"] == "Review":
            review += 1
        else:
            escalate += 1

        total_risk += r["risk_score"]

        if r.get("llm_used"):
            llm_runs += 1

    avg_risk = total_risk / len(results)

    print("\n===== EVALUATION METRICS =====")
    print("Total Cases:", len(results))
    print("High Risk:", high)
    print("Medium Risk:", medium)
    print("Low Risk:", low)
    print("Approve:", approve)
    print("Review:", review)
    print("Escalate:", escalate)
    print("Average Risk Score:", avg_risk)
    print("LLM Explanations Generated:", llm_runs)
    print("Processing Time:", processing_time)