
import streamlit as st
import requests

# Cloud Run API endpoint
API_URL = "https://orchestrator-agent-329609356017.asia-southeast1.run.app/run_pipeline"

st.set_page_config(
    page_title="ML Gatekeeper",
    page_icon="🛡️",
    layout="wide"
)

# ---------------- HEADER ----------------
st.title("🛡️ ML Gatekeeper")
st.subheader("AI Multi-Agent Pipeline Validator")

st.markdown("""
ML Gatekeeper analyzes ML pipelines using **AI agents**.

Pipeline Flow  
Extractor → Validator → Reviewer → Decision
""")

# ---------------- DEMO PIPELINE ----------------
demo_pipeline = """
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
"""

# ---------------- SIDEBAR ----------------
mode = st.sidebar.radio(
    "Choose Mode",
    ["Demo Pipeline", "Custom Pipeline"]
)

# ---------------- INPUT ----------------
if mode == "Demo Pipeline":

    st.info("Demo pipeline loaded")

    user_code = demo_pipeline

    st.code(user_code, language="python")

else:

    user_code = st.text_area(
        "Paste your ML pipeline code",
        height=250
    )

# ---------------- ANALYZE ----------------
if st.button("🚀 Analyze Pipeline"):

    if user_code.strip() == "":
        st.warning("Please enter pipeline code")

    else:

        with st.spinner("Running AI agents..."):

            try:

                payload = {"code": user_code}

                response = requests.post(
                    API_URL,
                    json=payload,
                    timeout=30
                )

                # Debug info
                st.write("API Status Code:", response.status_code)

                if response.status_code == 200:

                    result = response.json()

                    st.success("Pipeline analysis complete")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.subheader("🔍 Extractor Agent")
                        st.json(result.get("extraction", {}))

                    with col2:
                        st.subheader("🧪 Validation Agent")
                        st.json(result.get("validation", {}))

                    with col3:
                        st.subheader("🧠 Review Agent")
                        st.json(result.get("review", {}))

                    st.divider()

                    decision = result.get("decision", "unknown")

                    st.subheader("🛡️ Gatekeeper Decision")

                    if decision == "approved":
                        st.success("✅ Pipeline Approved")

                    elif decision == "warning":
                        st.warning("⚠️ Needs Review")

                    elif decision == "rejected":
                        st.error("❌ Pipeline Rejected")

                    else:
                        st.info("Decision not returned by API")

                else:

                    st.error("API returned an error")
                    st.text(response.text)

            except Exception as e:

                st.error("Connection failed")
                st.text(str(e))

# ---------------- FOOTER ----------------
st.divider()

st.markdown("""
### About ML Gatekeeper

ML Gatekeeper is a **multi-agent AI system** designed to audit ML pipelines.

Agents:

• Extractor Agent – Understands pipeline structure  
• Validation Agent – Checks ML best practices  
• Review Agent – Performs safety analysis  
""")

