import streamlit as st
from ml_pipeline import predict

# =================== Streamlit UI ===================
st.set_page_config(page_title="Health Insurance Cost Predictor", page_icon="💰", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
        .main {background-color: #f9fafc;}
        .stButton > button {width: 100%; border-radius: 12px; background-color: #4CAF50; color: white; font-size: 18px; padding: 10px;}
        .stButton > button:hover {background-color: #45a049; color: #fff;}
        .prediction-box {padding: 20px; border-radius: 12px; background-color: #eafaf1; border: 1px solid #4CAF50; font-size: 20px; font-weight: bold; text-align: center;}
    </style>
""", unsafe_allow_html=True)

st.title("💰 Health Insurance Cost Predictor")
st.write("Fill in your details below to estimate your expected **insurance cost**.")

with st.sidebar:
    st.header("ℹ️ About this app")
    st.write("This ML-powered app predicts your expected health insurance cost based on lifestyle, demographics, and health history.")
    st.info("👉 Enter all inputs and hit **Predict** to see the result.")

categorical_options = {
    'Gender':['Male','Female'],
    'Marital Status':['Unmarried','Married'],
    'BMI Category':['Normal','Obesity','Overweight','Underweight'],
    'Smoking Status':['No Smoking','Regular','Occasional'],
    'Employment Status':['Salaried','Self-Employed','Freelancer',''],
    'Region':['Northwest','Southeast','Northeast','Southwest'],
    'Medical History':['No Disease','Diabetes','High blood pressure','Diabetes & High blood pressure','Thyroid','Heart disease','High blood pressure & Heart disease','Diabetes & Thyroid','Diabetes & Heart disease'],
    'Insurance Plan':['Bronze','Silver','Gold']
}

with st.form("prediction_form"):
    st.subheader("📝 Personal Information")
    col1,col2,col3 = st.columns(3)
    age = col1.number_input('Age',18,100)
    number_of_dependants = col2.number_input('Number of Dependants',0,20)
    income_lakhs = col3.number_input('Income in Lakhs',0,200)

    st.subheader("⚕️ Health & Lifestyle")
    col4,col5,col6 = st.columns(3)
    genetical_risk = col4.number_input('Genetical Risk',0,5)
    bmi_category = col5.selectbox('BMI Category', categorical_options['BMI Category'])
    smoking_status = col6.selectbox('Smoking Status', categorical_options['Smoking Status'])

    col7,col8,col9 = st.columns(3)
    gender = col7.selectbox('Gender', categorical_options['Gender'])
    marital_status = col8.selectbox('Marital Status', categorical_options['Marital Status'])
    medical_history = col9.selectbox('Medical History', categorical_options['Medical History'])

    st.subheader("💼 Financial & Coverage")
    col10,col11,col12 = st.columns(3)
    insurance_plan = col10.selectbox('Insurance Plan', categorical_options['Insurance Plan'])
    employment_status = col11.selectbox('Employment Status', categorical_options['Employment Status'])
    region = col12.selectbox('Region', categorical_options['Region'])

    submitted = st.form_submit_button("🚀 Predict")

input_dict = {
    'Age': age, 'Number of Dependants': number_of_dependants, 'Income in Lakhs': income_lakhs,
    'Genetical Risk': genetical_risk, 'Insurance Plan': insurance_plan, 'Employment Status': employment_status,
    'Gender': gender, 'Marital Status': marital_status, 'BMI Category': bmi_category,
    'Smoking Status': smoking_status, 'Region': region, 'Medical History': medical_history
}

if submitted:
    prediction = predict(input_dict)
    st.markdown(f"<div class='prediction-box'>Predicted Health Insurance Cost: ₹ {prediction:,}</div>", unsafe_allow_html=True)
