```python
import streamlit as st
import requests
import json

# Cloud Run Orchestrator API
API_URL = "https://orchestrator-agent-329609356017.asia-southeast1.run.app/analyze_pipeline"

st.set_page_config(
    page_title="ML Gatekeeper",
    page_icon="🛡️",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
h1 {
    color: #38bdf8;
}
.stButton>button {
    background-color: #38bdf8;
    color: black;
    font-weight: bold;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Header
# -----------------------------
st.title("🛡️ ML Gatekeeper")
st.subheader("AI Multi-Agent Pipeline Validator")

st.markdown("""
ML Gatekeeper analyzes machine learning pipelines using **autonomous AI agents**.

### Pipeline Flow
Extractor Agent → Validation Agent → Review Agent → Final Decision
""")

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.title("⚙️ Controls")

mode = st.sidebar.radio(
    "Choose Mode",
    ["Custom Pipeline", "Demo Pipeline"]
)

# -----------------------------
# Sample Pipeline
# -----------------------------
demo_pipeline = """
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
"""

# -----------------------------
# Input
# -----------------------------
if mode == "Custom Pipeline":

    user_code = st.text_area(
        "Paste your ML pipeline code",
        height=250
    )

else:

    st.info("Demo pipeline loaded. Click analyze to run all agents.")

    user_code = demo_pipeline

    st.code(user_code, language="python")

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🚀 Analyze Pipeline"):

    if user_code.strip() == "":
        st.warning("Please enter pipeline code.")
    else:

        with st.spinner("Running AI Agents..."):

            try:

                payload = {"code": user_code}

                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:

                    result = response.json()

                    st.success("Pipeline Analysis Complete")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.subheader("🔍 Extractor Agent")
                        st.json(result.get("extraction"))

                    with col2:
                        st.subheader("🧪 Validation Agent")
                        st.json(result.get("validation"))

                    with col3:
                        st.subheader("🧠 Review Agent")
                        st.json(result.get("review"))

                    st.divider()

                    st.subheader("🛡️ Final Gatekeeper Decision")

                    decision = result.get("decision", "Unknown")

                    if decision == "approved":
                        st.success("✅ Pipeline Approved")

                    elif decision == "warning":
                        st.warning("⚠️ Pipeline Needs Review")

                    else:
                        st.error("❌ Pipeline Rejected")

                else:
                    st.error("API Error")

            except Exception as e:

                st.error("Connection failed")
                st.write(e)

# -----------------------------
# Footer
# -----------------------------
st.divider()

st.markdown(
"""
### 🚀 About ML Gatekeeper

ML Gatekeeper is a **multi-agent AI system** that automatically audits machine learning pipelines.

Agents used:

• Extractor Agent – understands pipeline structure  
• Validation Agent – checks best practices  
• Review Agent – performs AI safety analysis  

Built for **secure and reliable AI deployment**.
"""
)
```
