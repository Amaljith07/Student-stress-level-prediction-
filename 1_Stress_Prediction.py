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
        </style>
        """,
        unsafe_allow_html=True
    )
set_bg("background.png")    
import streamlit as st
import pickle

st.title("🎯 Stress Level Prediction")

model_data = pickle.load(open("student_stress_level_model.pkl", "rb"))
model = model_data["model"]
le_gender = model_data["le_gender"]
le_academic = model_data["le_academic"]
le_social = model_data["le_social"]
le_financial = model_data["le_financial"]
le_family = model_data["le_family"]
le_physical = model_data["le_physical"]
le_stress = model_data["le_stress"]

col1, col2 = st.columns(2)

with col1:
    age = st.number_input("Age", 10, 30)
    gender = st.selectbox("Gender", le_gender.classes_)
    academic_status = st.selectbox("Academic Year", le_academic.classes_)
    sleep_hours = st.number_input("Sleep Hours", 0.0, 12.0, step=0.5)
    physical_activity = st.selectbox("Physical Activity", le_physical.classes_)

with col2:
    study_hours = st.number_input("Study Hours", 0.0, 12.0, step=0.5)
    social_activity = st.selectbox("Social Activity", le_social.classes_)
    financial_status = st.selectbox("Financial Stress", le_financial.classes_)
    cgpa = st.number_input("CGPA", 0.0, 10.0)
    family_support = st.selectbox("Family Support", le_family.classes_)

internet_usage = st.number_input("Internet Usage (hours/day)", 0.0, 15.0, step=0.5)
exam_anxiety = st.number_input("Exam Anxiety (0-10)", 0.0, 10.0, step=0.1)

if st.button("Predict Stress Level"):

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

    st.success(f"🎓 Predicted Stress Level: **{stress_level}**")

    stress_from_sleep = 8 - sleep_hours
    study_sleep_ratio = round(study_hours / sleep_hours, 2) if sleep_hours > 0 else "NA"
    activity_map = {"Low": 2, "Medium": 1, "High": 0}
    activity_score = activity_map[physical_activity]
    health_risk = stress_from_sleep + activity_score

    st.write("### 📊 Advanced Insights")
    st.write(f"- **Stress From Sleep:** {stress_from_sleep}")
    st.write(f"- **Study/Sleep Ratio:** {study_sleep_ratio}")
    st.write(f"- **Physical Activity Score:** {activity_score}")
    st.write(f"- **Health Risk Score:** {health_risk}")