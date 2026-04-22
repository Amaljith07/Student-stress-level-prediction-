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

st.title("ℹ️ About This App")

st.write("""
### 🎓 Student Stress Predictor

This application predicts a student's stress level using:
- Sleep patterns  
- Study habits  
- Physical activity  
- Social activity  
- Financial stress  
- Family support  
- Internet usage  
- Academic year  
- Exam anxiety  

### 🧠 ML Model Used
**XGBoost Classifier** trained on student lifestyle and stress dataset.

### 📊 Additional Calculations
- Stress From Sleep  
- Study–Sleep Ratio  
- Physical Activity Score  
- Health Risk Score  
""")