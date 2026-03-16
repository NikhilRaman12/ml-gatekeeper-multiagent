from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
import requests

app = FastAPI()

# Replace with your orchestrator Cloud Run URL
ORCHESTRATOR_URL = "https://orchestrator-agent-204792553419.us-central1.run.app/process"
@app.get("/", response_class=HTMLResponse)
def form():
    return """
    <html>
      <head>
        <title>Multi-Agent System Demo</title>
      </head>
      <body style="font-family: Arial; margin: 40px;">
        <h2>Multi-Agent System Demo</h2>
        <form action="/submit" method="post">
          <label>Enter your task:</label><br>
          <input type="text" name="task" size="60"><br><br>
          <input type="submit" value="Run Pipeline">
        </form>
      </body>
    </html>
    """

@app.post("/submit", response_class=HTMLResponse)
def submit(task: str = Form(...)):
    payload = {"task": task}
    try:
        resp = requests.post(ORCHESTRATOR_URL, json=payload, timeout=30)
        result = resp.json()
    except Exception as e:
        result = {"error": str(e)}

    return f"""
    <html>
      <head><title>Pipeline Result</title></head>
      <body style="font-family: Arial; margin: 40px;">
        <h3>Task:</h3>
        <pre>{task}</pre>
        <h3>Result:</h3>
        <pre>{result}</pre>
        <br><a href="/">Back</a>
      </body>
    </html>
    """

@app.get("/ping")
def ping():
    return {"status": "ok"}