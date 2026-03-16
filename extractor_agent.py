import requests

# Use the actual Cloud Run URL
ORCHESTRATOR_URL = "https://orchestrator-agent-204792553419.us-central1.run.app/pipeline"

payload = {"code": "print(\"hello world\")"}
headers = {"Content-Type": "application/json"}

try:
    resp = requests.post(ORCHESTRATOR_URL, json=payload, headers=headers)
    resp.raise_for_status()
    print("Pipeline response:")
    print(resp.json())
except requests.exceptions.RequestException as e:
    print(f"Error calling orchestrator: {e}")