import streamlit as st
import requests
from PIL import Image

# 🔗 Backend Orchestrator URL (UPDATE if needed)
BACKEND_URL = "https://orchestrator-agent-329609356017.asia-southeast1.run.app"

# 🎨 Page Config
st.set_page_config(
    page_title="DevSecOps Agent Flow Studio",
    layout="wide"
)

# 🧠 Title & Description
st.title("DevSecOps Agent Flow Studio")
st.subheader("AI Agents: Extractor → Validator → Reviewer → Deployment Decision")

st.write("""
This demo showcases a multi-agent DevSecOps pipeline built on GitLab.

Paste your ML pipeline code → Agents analyze → Get validation, risks, and deployment decision.
""")

# 📌 Default ML Pipeline Code
default_code = """from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('pca', PCA(n_components=2)),
    ('model', LogisticRegression())
])
"""

# ✍️ Code Input
code = st.text_area(
    "Paste or edit your ML pipeline code:",
    value=default_code,
    height=250
)

# 🖼️ Optional Image Upload
uploaded_img = st.file_uploader(
    "Upload a pipeline diagram (optional)",
    type=["png", "jpg", "jpeg"]
)

if uploaded_img:
    image = Image.open(uploaded_img)
    st.image(image, caption="Uploaded Pipeline Diagram", use_column_width=True)

# 🚀 Run Analysis
if st.button("Analyze Pipeline"):
    if code.strip():

        with st.spinner("Running AI Agent Flow..."):

            payload = {"code": code}

            try:
                # ✅ Call ORCHESTRATOR (correct endpoint)
                response = requests.post(
                    f"{BACKEND_URL}/process",
                    json=payload,
                    timeout=60
                )

                if response.status_code == 200:
                    result = response.json()

                    st.success("Pipeline Analysis Completed")

                    # 📊 Show Full Result
                    st.subheader("Full Agent Output")
                    st.json(result)

                    # 🎯 Extract Final Decision (if exists)
                    decision = result.get("result", {}).get("decision", None)

                    if decision:
                        st.subheader("Final Deployment Decision")
                        st.write(decision)

                else:
                    st.error(f"API Error {response.status_code}: {response.text}")

            except Exception as e:
                st.error(f"Connection Error: {e}")

    else:
        st.warning("Please paste pipeline code before analyzing.")

# 📌 Footer
st.markdown("---")
st.caption("Built for GitLab Duo Agent Platform Hackathon | DevSecOps Agents Flow Squad")
