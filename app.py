import streamlit as st
import base64

def set_bg(image_file):
    with open(image_file, "rb") as f:
        encoded_string = base64.b64encode(f.read()).decode()

    st.markdown(
    f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_string}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
    }}

    /* Make label text ABOVE inputs bold */
    label {{
        font-weight: bold !important;
        color: #121212 !important;
    }}
    </style>
    """,
    unsafe_allow_html=True
)


set_bg("background.png")    
import streamlit as st
import pickle
import numpy as np

# ------------------------------
# Load Model
# ------------------------------
model_data = pickle.load(open("student_stress_level_model.pkl", "rb"))
model = model_data["model"]
le_gender = model_data["le_gender"]
le_academic = model_data["le_academic"]
le_social = model_data["le_social"]
le_financial = model_data["le_financial"]
le_family = model_data["le_family"]
le_physical = model_data["le_physical"]
le_stress = model_data["le_stress"]

# ------------------------------
# Streamlit UI Styling
# ------------------------------
st.set_page_config(page_title="Student Stress Level Predictor", layout="centered")


st.markdown(
    """
    <h1 style='text-align: center; color:#121212;'> Student Stress Level Prediction App</h1>
    <p style='text-align: center; color:#121212; font-size:18px;'>Enter your details and get your predicted stress level instantly</p>
    <hr>
    """,
    unsafe_allow_html=True
)

# ------------------------------
# Input Form
# ------------------------------
st.markdown(
    "<h3 style='color:#121212; font-weight:bold;'>📝 Enter Your Details</h3>",
    unsafe_allow_html=True
)


col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", min_value=10, max_value=30, step=1)
    gender = st.selectbox("Gender", le_gender.classes_)
    academic_status = st.selectbox("Academic Year", le_academic.classes_)
    sleep_hours = st.number_input("Sleep Hours per day", min_value=0.0, max_value=15.0, step=0.5)
    physical_activity = st.selectbox("Physical Activity", le_physical.classes_)

with col2:
    study_hours = st.number_input("Study Hours per day", min_value=0.0, max_value=15.0, step=0.5)
    social_activity = st.selectbox("Social Activity", le_social.classes_)
    financial_status = st.selectbox("Financial Stress", le_financial.classes_)
    cgpa = st.number_input("CGPA", min_value=0.0, max_value=10.0, step=0.1)
    family_support = st.selectbox("Family Support", le_family.classes_)

internet_usage = st.number_input("Internet Usage (hours/day)", min_value=0.0, max_value=15.0, step=0.5)
exam_anxiety = st.number_input("Exam Anxiety (0–10)", min_value=0.0, max_value=10.0, step=0.1)


# ------------------------------
# Predict Button
# ------------------------------
if st.button("🎯 Predict Stress Level"):

    # Encode values
    gender_val = le_gender.transform([gender])[0]
    academic_val = le_academic.transform([academic_status])[0]
    physical_val = le_physical.transform([physical_activity])[0]
    social_val = le_social.transform([social_activity])[0]
    financial_val = le_financial.transform([financial_status])[0]
    family_val = le_family.transform([family_support])[0]

    user_data = [[age, gender_val, academic_val, sleep_hours, study_hours,
                  physical_val, social_val, financial_val, cgpa, family_val,
                  internet_usage, exam_anxiety]]

    prediction = model.predict(user_data)
    stress_level = le_stress.inverse_transform(prediction)[0]

    # ------------------------------
    # Advanced Feature Calculations
    # ------------------------------
    stress_from_sleep = 8 - sleep_hours
    study_sleep_ratio = round(study_hours / sleep_hours, 2) if sleep_hours > 0 else "Undefined"
    
    activity_map = {"Low": 2, "Medium": 1, "High": 0}
    physical_activity_level = activity_map[physical_activity]

    health_risk = stress_from_sleep + physical_activity_level

    # ------------------------------
    # Result Display
    # ------------------------------
    st.markdown(
        f"""
        <div style="padding:20px; border-radius:10px; background-color:#f2f2f2; text-align:center;">
            <h2 style="color:#FF5733;"> Predicted Stress Level: <b>{stress_level}</b> </h2>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown("<br><br><br><br>",unsafe_allow_html=True)
    st.markdown("<h3 style='color:#00c3ff;'>🔍 Advanced Feature Analysis</h3>", unsafe_allow_html=True)

st.markdown(f"<p style='font-size:18px; color:#121212;'><b>Stress From Sleep:</b> {stress_from_sleep}</p>", unsafe_allow_html=True)

st.markdown(f"<p style='font-size:18px; color:#121212;'><b>Study Sleep Ratio:</b> {study_sleep_ratio}</p>", unsafe_allow_html=True)

st.markdown(f"<p style='font-size:18px; color:#121212;'><b>Physical Activity Level:</b> {physical_activity_level}</p>", unsafe_allow_html=True)

st.markdown(f"<p style='font-size:18px; color:#121212;'><b>Health Risk Score:</b> {health_risk}</p>", unsafe_allow_html=True)