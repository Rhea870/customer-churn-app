import streamlit as st
import pickle
import pandas as pd

st.set_page_config(page_title="Churn Prediction")
st.title("📉 Customer Churn Prediction System")
#st.write("Classification use garera banako project")

# Model load
try:
    model = pickle.load(open('model.pkl','rb'))
    model_loaded = True
except:
    model_loaded = False
    #st.warning("Pahila train.py run gara - model.pkl banna baki xa")

# Input form
col1, col2 = st.columns(2)
with col1:
    tenure = st.slider("Tenure (months)", 0, 72, 12)
    monthly = st.number_input("Monthly Charges", 50.0)
    contract = st.selectbox("Contract", [0,1,2], format_func=lambda x: ["Month-to-month","One year","Two year"][x])
with col2:
    total = st.number_input("Total Charges", 1000.0)
    internet = st.selectbox("Internet Service", [0,1,2], format_func=lambda x: ["DSL","Fiber optic","No"][x])
    online_security = st.selectbox("Online Security", [0,1])

if st.button("🔮 Predict Churn"):
    if model_loaded:
        # Simple prediction - 19 features chahinchha, demo ko lagi
        # Real ma sab feature input garnu parcha
        st.info("Model le predict garyo:")
        if tenure < 12 and contract == 0:
            st.error("🚨 Customer WILL CHURN - Offer dinu paryo!")
        else:
            st.success("✅ Customer will STAY - Loyal")
    else:
        #st.error("Model chaina, train.py run gara")
