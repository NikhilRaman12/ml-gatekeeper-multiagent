# mlgatekeeper_app.py (Streamlit frontend)
import streamlit as st
import requests

# -----------------------------
# Streamlit UI
# -----------------------------
st.set_page_config(page_title="🛡️ ML Gatekeeper", layout="centered")

st.title("🛡️ ML Gatekeeper - AI Multi-Agent Pipeline Validator")
st.write("Analyze ML pipelines using Extractor → Validator → Reviewer → Decision")

# Text area for pipeline code
code = st.text_area("Paste your ML pipeline code:", height=200)

# Backend URL (FastAPI service)
BACKEND_URL = "http://localhost:8080"   # change to your Cloud Run URL if deployed

# Validate pipeline
if st.button("Validate Pipeline"):
    if code.strip():
        resp = requests.post(f"{BACKEND_URL}/validate", json={"code": code})
        st.subheader("Validation Result")
        st.json(resp.json())
    else:
        st.warning("Please paste pipeline code before validating.")

# Run pipeline
if st.button("Run Pipeline"):
    if code.strip():
        resp = requests.post(f"{BACKEND_URL}/run_pipeline", json={"code": code})
        result = resp.json()
        st.subheader("Pipeline Analysis Results")
        st.write("**Extractor Agent:**", result["extraction"])
        st.write("**Validation Agent:**", result["validation"])
        st.write("**Review Agent:**", result["review"])
        st.write("**Gatekeeper Decision:**", result["decision"])
    else:
        st.warning("Please paste pipeline code before running.")
