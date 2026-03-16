from fastapi import FastAPI
import requests

app = FastAPI()

# Downstream agent URLs
EXTRACTOR_URL = "https://extractor-agent-204792553419.us-central1.run.app"
VALIDATOR_URL = "https://validator-agent-204792553419.us-central1.run.app"
REVIEWER_URL  = "https://reviewer-agent-204792553419.us-central1.run.app"

@app.get("/")
def root():
    return {"message": "Orchestrator running successfully"}

@app.post("/process")
def process(data: dict):
    # Step 1: Extract
    extractor_resp = requests.post(
        f"{EXTRACTOR_URL}/analyze",
        json={"code": data.get("code", "")}
    )
    extracted = extractor_resp.json()

    # Step 2: Validate
    validator_resp = requests.post(f"{VALIDATOR_URL}/validate", json=extracted)
    validated = validator_resp.json()

    # Step 3: Review
    reviewer_resp = requests.post(f"{REVIEWER_URL}/review", json=validated)
    reviewed = reviewer_resp.json()

    return {"result": reviewed}