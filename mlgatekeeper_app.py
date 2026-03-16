import streamlit as st
import requests
from PIL import Image

BACKEND_URL = "https://orchestrator-agent-329609356017.asia-southeast1.run.app"

st.set_page_config(page_title="🛡️ ML Gatekeeper Demo", layout="wide")

st.title("🛡️ ML Gatekeeper - Multi-Agent Pipeline Validator")
st.write("Agents: Extractor → Validator → Reviewer → Decision")

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

uploaded_img = st.file_uploader("Upload a pipeline diagram (image)", type=["png","jpg","jpeg"])
if uploaded_img:
    image = Image.open(uploaded_img)
    st.image(image, caption="Uploaded Pipeline Diagram", use_column_width=True)

if st.button("🚀 Analyze Pipeline"):
    if code.strip():
        # ✅ Use /validate and send {"code": ...}
        payload = {"code": code}
        resp = requests.post(f"{BACKEND_URL}/validate", json=payload)

        if resp.status_code == 200:
            result = resp.json()
            st.subheader("Validation Result")
            st.json(result)
        else:
            st.error(f"API Error {resp.status_code}: {resp.text}")
    else:
        st.warning("Please paste pipeline code before analyzing.")
