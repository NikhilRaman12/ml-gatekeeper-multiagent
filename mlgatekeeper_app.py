# mlgatekeeper_app.py
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict, Any
import uvicorn

app = FastAPI(title="MLGatekeeper API")

# -----------------------------
# Schemas
# -----------------------------
class PipelineStep(BaseModel):
    name: str
    type: str
    parameters: Dict[str, Any] = {}

class PipelineInput(BaseModel):
    code: str  # The Python code of the pipeline

class AgentResult(BaseModel):
    extraction: Dict[str, Any]
    validation: Dict[str, Any]
    review: Dict[str, Any]
    decision: str

# -----------------------------
# Routes
# -----------------------------
@app.get("/")
def root():
    return {"message": "MLGatekeeper API is running!"}

@app.post("/validate")
def validate_pipeline(pipeline: PipelineInput):
    # Simple validation logic
    if not pipeline.code.strip():
        return {"valid": False, "message": "Pipeline code is empty."}
    return {"valid": True, "message": "Pipeline code is present."}

@app.post("/run_pipeline", response_model=AgentResult)
def run_pipeline(pipeline: PipelineInput):
    code = pipeline.code

    # ---------------- Agents Simulation ----------------
    # Extractor Agent
    extraction = {"steps_found": ["scaler", "model"] if "Pipeline" in code else []}

    # Validation Agent
    validation = {"best_practices": "Passed" if "Pipeline" in code else "Failed"}

    # Review Agent
    review = {"safety_checks": "No issues detected" if "Pipeline" in code else "Issues detected"}

    # Gatekeeper Decision Logic
    if extraction["steps_found"] and validation["best_practices"] == "Passed":
        decision = "approved"
    elif extraction["steps_found"]:
        decision = "warning"
    else:
        decision = "rejected"

    return {
        "extraction": extraction,
        "validation": validation,
        "review": review,
        "decision": decision
    }

# -----------------------------
# Run
# -----------------------------
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
