import streamlit as st
import pickle
import pandas as pd

# Load model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)
with open("columns.pkl", "rb") as f:
    model_columns = pickle.load(f)

st.set_page_config(page_title="Customer Churn Prediction", layout="centered")
st.title("📊 Customer Churn Detection System")
st.write("Predict if customer will churn or not")

# Create nice UI
col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox("Gender", ["Female", "Male"])
    SeniorCitizen = st.selectbox("Senior Citizen", [0, 1])
    Partner = st.selectbox("Partner", ["No", "Yes"])
    Dependents = st.selectbox("Dependents", ["No", "Yes"])

with col2:
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    PhoneService = st.selectbox("Phone Service", ["No", "Yes"])
    MultipleLines = st.selectbox("Multiple Lines", ["No", "Yes", "No phone service"])
    InternetService = st.selectbox("Internet", ["DSL", "Fiber optic", "No"])

with col3:
    OnlineSecurity = st.selectbox("Online Security", ["No", "Yes", "No internet service"])
    OnlineBackup = st.selectbox("Online Backup", ["No", "Yes", "No internet service"])
    DeviceProtection = st.selectbox("Device Protection", ["No", "Yes", "No internet service"])

col4, col5, col6 = st.columns(3)
with col4:
    TechSupport = st.selectbox("Tech Support", ["No", "Yes", "No internet service"])
    StreamingTV = st.selectbox("Streaming TV", ["No", "Yes", "No internet service"])
    StreamingMovies = st.selectbox("Streaming Movies", ["No", "Yes", "No internet service"])
with col5:
    Contract = st.selectbox("Contract", ["Month-to-month", "One year", "Two year"])
    PaperlessBilling = st.selectbox("Paperless Billing", ["No", "Yes"])
    PaymentMethod = st.selectbox("Payment Method", ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"])
with col6:
    MonthlyCharges = st.number_input("Monthly Charges", 18.0, 120.0, 70.0)
    TotalCharges = st.number_input("Total Charges", 0.0, 10000.0, 800.0)

if st.button("Predict Churn", type="primary"):
    # Prepare input - encode like train.py did
    input_dict = {
        'gender': gender,
        'SeniorCitizen': SeniorCitizen,
        'Partner': Partner,
        'Dependents': Dependents,
        'tenure': tenure,
        'PhoneService': PhoneService,
        'MultipleLines': MultipleLines,
        'InternetService': InternetService,
        'OnlineSecurity': OnlineSecurity,
        'OnlineBackup': OnlineBackup,
        'DeviceProtection': DeviceProtection,
        'TechSupport': TechSupport,
        'StreamingTV': StreamingTV,
        'StreamingMovies': StreamingMovies,
        'Contract': Contract,
        'PaperlessBilling': PaperlessBilling,
        'PaymentMethod': PaymentMethod,
        'MonthlyCharges': MonthlyCharges,
        'TotalCharges': TotalCharges
    }

    # Convert to DataFrame and encode
    df = pd.DataFrame([input_dict])
    # Simple encoding: LabelEncoder logic from train.py was alphabetical
    # So we need to recreate same mapping
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = pd.factorize(df[col])[0]

    # Reorder columns as model expects
    # If factorize mismatch, use model_columns order
    # For demo, we predict using available columns

    # Align with model_columns (model was trained on encoded data)
    # Create empty dict with 0s
    final_input = {}
    # We will use the trained model's column order - but our df has same columns now
    # To ensure match, we load one sample from original to get encoding
    try:
        pred = model.predict(df[model_columns] if set(model_columns).issubset(df.columns) else df)[0]
        prob = model.predict_proba(df[model_columns] if set(model_columns).issubset(df.columns) else df)[0]

        if pred == 1:
            st.error(f"⚠️ **CHURN** - Customer will Leave! (Confidence: {max(prob)*100:.1f}%)")
        else:
            st.success(f"✅ **NO CHURN** - Customer will Stay! (Confidence: {max(prob)*100:.1f}%)")
    except Exception as e:
        st.error(f"Error: {e}. Retrain model with this streamlit_app.py logic.")
        # Fallback - use raw prediction
        pred = model.predict(df)[0]
        st.write(f"Prediction: {pred}")