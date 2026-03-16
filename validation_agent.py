from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class PipelineInput(BaseModel):
    code: str

@app.get("/")
def root():
    return {"message": "Validator running successfully"}

@app.post("/validate")
async def validate(input: PipelineInput):
    try:
        issues = []
        risk_level = "low"
        recommendations = ["Pipeline looks valid"]

        # Example rule: flag risky imports
        if "import os" in input.code or "import subprocess" in input.code:
            issues.append("Potentially unsafe import detected")
            risk_level = "medium"
            recommendations.append("Avoid direct system calls")

        return {
            "issues": issues,
            "risk_level": risk_level,
            "recommendations": recommendations,
            "input_received": input.code
        }
    except Exception as e:
        return {
            "issues": ["Validator crashed"],
            "risk_level": "unknown",
            "recommendations": ["Check logs"],
            "error": str(e)
        }