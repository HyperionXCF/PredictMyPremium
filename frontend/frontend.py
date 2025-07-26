import streamlit as st 
import requests

API_URL = "https://predictmypremium.onrender.com/predict"

st.title("Insurance Premium Category Predictor")

st.markdown("Enter your details below : ")

# input fields

age = st.number_input("Age",min_value=1,max_value=119,value=30)
weight = st.number_input("Weight",min_value=1.0,max_value=120.0)
height = st.number_input("Height",min_value=0.5,max_value=2.5,value=1.7)
income_lpa = st.number_input("Annual Income in LPA",min_value=0.1, value=10.0)
smoker = st.selectbox("Are you a smoker?",options=[True,False])
city = st.text_input("City",value="Mumbai")
occupation = st.selectbox(
    "Occupation",
    ["retired","business_owner","unemployed","private_job"]
)

if st.button("Predict Premium Category"):
    input_data = {
        "age" : age,
        "weight" : weight,
        "height" : height,
        "income_lpa" : income_lpa,
        "smoker" : smoker,
        "user_city" : city,
        "occupation" : occupation
    }


    try:
        response = requests.post(API_URL,json = input_data)
        if response.status_code == 200:
            result = response.json()
            st.success(f"Predicted Insurance Premium Category : **{result['predicted_category']}**")
        else:
            st.error(f"API Error : {response.status_code} - {response.text}")
    except requests.exceptions.ConnectionError:
        st.error("could not connect to fastAPI server. Make sure its running on port 8000")
