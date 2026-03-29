from orchestration.pipeline import Pipeline
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    print("\n===== SOCRATIC LEDGER PIPELINE STARTED =====\n")

    pipeline = Pipeline()

    result = pipeline.run(
        cik="320193",
        sec_user_agent=os.getenv("SEC_USER_AGENT")
    )

    print("\n===== FINAL OUTPUT =====")
    print(result)

    print("\n===== PIPELINE COMPLETED =====")