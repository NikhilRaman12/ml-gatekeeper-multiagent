```python
import streamlit as st
import requests

# Cloud Run API
API_URL = "https://orchestrator-agent-329609356017.asia-southeast1.run.app/analyze_pipeline"

st.set_page_config(
    page_title="ML Gatekeeper",
    page_icon="🛡️",
    layout="wide"
)

# --------- HEADER ---------
st.title("🛡️ ML Gatekeeper")
st.subheader("AI Multi-Agent Pipeline Validator")

st.markdown(
"""
ML Gatekeeper analyzes machine learning pipelines using **multiple AI agents**.

**Pipeline Flow**

Extractor Agent → Validation Agent → Review Agent → Final Decision
"""
)

# --------- DEMO PIPELINE ---------
demo_pipeline = """
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
"""

# --------- SIDEBAR ---------
st.sidebar.header("Controls")

mode = st.sidebar.radio(
    "Choose Mode",
    ["Demo Pipeline", "Custom Pipeline"]
)

# --------- INPUT ---------
if mode == "Demo Pipeline":
    st.info("Demo ML pipeline loaded")

    user_code = demo_pipeline

    st.code(user_code, language="python")

else:
    user_code = st.text_area(
        "Paste your ML pipeline code",
        height=250
    )

# --------- ANALYZE BUTTON ---------
if st.button("Analyze Pipeline 🚀"):

    if user_code.strip() == "":
        st.warning("Please enter pipeline code")
    else:

        with st.spinner("Running AI Agents..."):

            try:
                payload = {"code": user_code}

                response = requests.post(API_URL, json=payload)

                if response.status_code == 200:

                    result = response.json()

                    st.success("Pipeline analysis complete")

                    col1, col2, col3 = st.columns(3)

                    with col1:
                        st.subheader("Extractor Agent")
                        st.json(result.get("extraction", {}))

                    with col2:
                        st.subheader("Validation Agent")
                        st.json(result.get("validation", {}))

                    with col3:
                        st.subheader("Review Agent")
                        st.json(result.get("review", {}))

                    st.divider()

                    decision = result.get("decision", "Unknown")

                    st.subheader("Final Gatekeeper Decision")

                    if decision == "approved":
                        st.success("Pipeline Approved")

                    elif decision == "warning":
                        st.warning("Pipeline Needs Review")

                    else:
                        st.error("Pipeline Rejected")

                else:
                    st.error("API request failed")

            except Exception as e:
                st.error("Connection error")
                st.write(e)

# --------- FOOTER ---------
st.divider()

st.markdown(
"""
### About ML Gatekeeper

ML Gatekeeper is a **multi-agent AI system** designed to audit machine learning pipelines.

Agents:

• Extractor Agent – Understands pipeline structure  
• Validation Agent – Checks ML best practices  
• Review Agent – Performs safety analysis  
"""
)
```
