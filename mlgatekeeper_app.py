# streamlit_app.py
import streamlit as st
import requests
from PIL import Image

BACKEND_URL = "https://orchestrator-agent-329609356017.asia-southeast1.run.app"

# -----------------------------
# Page Setup
# -----------------------------
st.set_page_config(page_title="🛡️ ML Gatekeeper Demo", layout="wide")

st.markdown(
    """
    <style>
    .main {background-color: #f9f9f9;}
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🛡️ ML Gatekeeper")
st.subheader("AI Multi-Agent Pipeline Validator")
st.write("**Agents:** Extractor → Validator → Reviewer → Decision")

# -----------------------------
# Input Section
# -----------------------------
col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📄 Paste ML Pipeline Code")
    default_code = """from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipeline = Pipeline([
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])
"""
    code = st.text_area("Pipeline Code:", value=default_code, height=200)

with col2:
    st.markdown("### 🖼️ Upload Pipeline Diagram")
    uploaded_img = st.file_uploader("Upload an image", type=["png","jpg","jpeg"])
    if uploaded_img:
        image = Image.open(uploaded_img)
        st.image(image, caption="Uploaded Pipeline Diagram", use_column_width=True)

# -----------------------------
# Action Buttons
# -----------------------------
st.markdown("---")
if st.button("🚀 Analyze Pipeline"):
    if code.strip():
        payload = {"pipeline": code}
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
