import requests

# Point to the correct orchestrator route
ORCHESTRATOR_URL = "https://orchestrator-agent-204792553419.us-central1.run.app/process"

payload = {"code": "print(\"hello world\")"}
headers = {"Content-Type": "application/json"}

def test_orchestration():
    response = requests.post(ORCHESTRATOR_URL, json=payload, headers=headers)
    response.raise_for_status()
    print("Pipeline response:")
    print(response.json())

if __name__ == "__main__":
    test_orchestration()