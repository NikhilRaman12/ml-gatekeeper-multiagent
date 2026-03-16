import os
from google.genai import Client
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

load_dotenv()
app = FastAPI()

# Initialize Gemini client
load_dotenv()
client = Client(api_key=os.getenv("GENAI_API_KEY"))
class ValidationReport(BaseModel):
    result: str

@app.get("/")
def root():
    return {"message": "Reviewer running successfully"}

@app.post("/review")
async def review(data: ValidationReport):
    prompt = f"""
You are a principal ML reviewer.

Based on the validation report below:

Provide:
- Final approval status (Approved / Needs Revision / High Risk)
- Production readiness score (0-100)
- Strategic improvements

Return structured JSON.

Validation Report:
{data.result}
"""
    try:
        response = client.models.generate_content(
    model="gemini-3.1-pro-preview",
    contents=prompt
)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini error: {str(e)}")