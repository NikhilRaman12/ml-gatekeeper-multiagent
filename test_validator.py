import requests

url = "https://validator-agent-204792553419.us-central1.run.app/validate"
payload = {"code": "print('hello world')"}
resp = requests.post(url, json=payload)

print("Status:", resp.status_code)
print("Raw text:", resp.text)