import streamlit as st
import skops.io as sio
import warnings
from sklearn.exceptions import InconsistentVersionWarning

# Suppress version warnings
warnings.filterwarnings("ignore", category=InconsistentVersionWarning)

# Trusted types for skops loading
trusted_types = [
    "sklearn.pipeline.Pipeline",
    "sklearn.preprocessing.OneHotEncoder",
    "sklearn.preprocessing.StandardScaler",
    "sklearn.compose.ColumnTransformer",
    "sklearn.preprocessing.OrdinalEncoder",
    "sklearn.impute.SimpleImputer",
    "sklearn.tree.DecisionTreeClassifier",
    "sklearn.ensemble.RandomForestClassifier",
    "numpy.dtype",
]

# Load trained pipeline model
pipe = sio.load("./Model/drug_pipeline.skops", trusted=trusted_types)

st.set_page_config(page_title="Drug Classification", page_icon="💊", layout="centered")

st.title("💊 Drug Classification AI")
st.write("Predict the recommended medication based on patient clinical parameters.")

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 15, 74, 30)
    sex = st.radio("Sex", ["M", "F"])
    bp = st.radio("Blood Pressure", ["HIGH", "LOW", "NORMAL"])

with col2:
    chol = st.radio("Cholesterol", ["HIGH", "NORMAL"])
    na_to_k = st.slider("Sodium to Potassium Ratio (Na_to_K)", 6.2, 38.2, 15.4, step=0.1)

if st.button("Predict Medication", type="primary", use_container_width=True):
    features = [age, sex, bp, chol, na_to_k]
    predicted = pipe.predict([features])[0]
    st.success(f"### Predicted Prescription: **{predicted}**")

st.markdown("---")
st.caption("Powered by Scikit-Learn Random Forest Pipeline & Deployed via Streamlit Community Cloud")
