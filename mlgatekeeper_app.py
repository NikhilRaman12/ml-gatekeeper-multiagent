# streamlit_app.py
import streamlit as st
import requests
from PIL import Image

# Backend URL (your deployed orchestrator)
BACKEND_URL = "https://orchestrator-agent-329609356017.asia-southeast1.run.app"

st.set_page_config(page_title="🛡️ ML Gatekeeper Demo", layout="wide")

st.title("🛡️ ML Gatekeeper - Multi-Agent Pipeline Validator")
st.write("Analyze ML pipelines using Extractor → Validator → Reviewer → Decision")

# -----------------------------
# Text Input
# -----------------------------
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
code = st.text_area("Paste or edit your ML pipeline code:", value=default_code, height=200)

# -----------------------------
# Image Input
# -----------------------------
uploaded_img = st.file_uploader("Upload a pipeline diagram (image)", type=["png","jpg","jpeg"])
if uploaded_img:
    image = Image.open(uploaded_img)
    st.image(image, caption="Uploaded Pipeline Diagram", use_column_width=True)

# -----------------------------
# Analyze Button
# -----------------------------
if st.button("🚀 Analyze Pipeline"):
    if code.strip():
        payload = {"pipeline": code}  # ✅ correct field name
        resp = requests.post(f"{BACKEND_URL}/analyze_pipeline", json=payload)

        if resp.status_code == 200:
            result = resp.json()
            st.markdown("## 🔎 Analysis Results")

            # Show agent outputs in tabs
            tab1, tab2, tab3, tab4 = st.tabs(["Extractor", "Validator", "Reviewer", "Decision"])

            with tab1:
                st.json(result.get("extraction"))

            with tab2:
                st.json(result.get("validation"))

            with tab3:
                st.json(result.get("review"))

            with tab4:
                decision = result.get("decision", "").lower()
                if decision == "approved":
                    st.success("✅ Pipeline Approved")
                elif decision == "warning":
                    st.warning("⚠️ Pipeline Warning")
                else:
                    st.error("❌ Pipeline Rejected")
        else:
            st.error(f"API Error {resp.status_code}: {resp.text}")
    else:
        st.warning("Please paste pipeline code before analyzing.")
