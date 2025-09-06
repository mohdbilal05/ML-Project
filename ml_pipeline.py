import pandas as pd
import joblib

# Load ML Artifacts
model_young = joblib.load("artifacts/model_young.joblib")
model_rest = joblib.load("artifacts/model_rest.joblib")
scaler_young = joblib.load("artifacts/scaler_young.joblib")
scaler_rest = joblib.load("artifacts/scaler_rest.joblib")

def calculate_normalized_risk(medical_history):
    risk_scores = {"diabetes": 6, "heart disease": 8, "high blood pressure": 6,
                   "thyroid": 5, "no disease": 0, "none": 0}
    diseases = medical_history.lower().split(" & ")
    return sum(risk_scores.get(d, 0) for d in diseases) / 14

def handle_scaling(age, df):
    scaler_object = scaler_young if age <= 25 else scaler_rest
    df['income_level'] = None
    df[scaler_object['cols_to_scale']] = scaler_object['scaler'].transform(df[scaler_object['cols_to_scale']])
    return df.drop('income_level', axis=1)

def preprocess_input(input_dict):
    expected_columns = [
        'age','number_of_dependants','income_lakhs','insurance_plan','genetical_risk','normalized_risk_score',
        'gender_Male','region_Northwest','region_Southeast','region_Southwest','marital_status_Unmarried',
        'bmi_category_Obesity','bmi_category_Overweight','bmi_category_Underweight','smoking_status_Occasional',
        'smoking_status_Regular','employment_status_Salaried','employment_status_Self-Employed'
    ]
    df = pd.DataFrame(0, columns=expected_columns, index=[0])
    enc = {'Bronze':1,'Silver':2,'Gold':3}
    mapping = {
        ('Gender','Male'):'gender_Male', ('Region','Northwest'):'region_Northwest',
        ('Region','Southeast'):'region_Southeast', ('Region','Southwest'):'region_Southwest',
        ('Marital Status','Unmarried'):'marital_status_Unmarried', ('BMI Category','Obesity'):'bmi_category_Obesity',
        ('BMI Category','Overweight'):'bmi_category_Overweight', ('BMI Category','Underweight'):'bmi_category_Underweight',
        ('Smoking Status','Occasional'):'smoking_status_Occasional', ('Smoking Status','Regular'):'smoking_status_Regular',
        ('Employment Status','Salaried'):'employment_status_Salaried', ('Employment Status','Self-Employed'):'employment_status_Self-Employed'
    }
    for (k,v),col in mapping.items():
        if input_dict.get(k) == v: df[col] = 1

    df['insurance_plan'] = enc.get(input_dict['Insurance Plan'],1)
    df['age'] = input_dict['Age']
    df['number_of_dependants'] = input_dict['Number of Dependants']
    df['income_lakhs'] = input_dict['Income in Lakhs']
    df['genetical_risk'] = input_dict['Genetical Risk']
    df['normalized_risk_score'] = calculate_normalized_risk(input_dict['Medical History'])
    return handle_scaling(input_dict['Age'], df)

def predict(input_dict):
    input_df = preprocess_input(input_dict)
    model = model_young if input_dict['Age'] <= 25 else model_rest
    return int(model.predict(input_df)[0])
