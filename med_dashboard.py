import streamlit as st
from google import genai
import os

Key = "AIzaSyA12uqVb3bEkeR4UdMPpiraAg2Wy8SMg8g"
input_message = """
    Top predicted class: **Healthy** (14.9% confidence)

Class probabilities:
  Healthy                  : 14.90%
  URTI                     : 14.63%
  Asthma & Lung Fibrosis   : 10.61%
  Pneumonia                : 10.19%
  Heart Failure            : 6.68%
  Heart Failure & Lung Fibrosis: 5.62%
  Bronchiolitis            : 5.52%
  Pleural Effusion         : 5.16%
  Bronchitis               : 5.09%
  Lung Fibrosis            : 4.89%
  LRTI                     : 3.94%
  Asthma                   : 3.70%
  Heart Failure & COPD     : 3.38%
  COPD                     : 2.95%
  Bronchiectasis           : 2.73%
  Give a summary of the above respository predictions in a way a patient with no medicate knowledge can understand. The probalities are a probability distribution from the ai model"""

client = genai.Client(api_key=Key)
response = client.models.generate_content(
    model="gemma-3-27b-it", contents=input_message
)
summary = response.text


#Data 


patient = {"Name": "John Doe","Age":58,"Gender": "Male","BMI":29.7}
pateint_info = "<div>"
pateint_info += "".join(
    f"""<div class="patient-info">{key}: {value}</div>"""
    for key,value in patient.items()
)
pateint_info += "</div>"

image_html = """
        <div class="image-container">
            <div class="image-content">
                <img src="./patient-pic.jpeg" 
                     alt="Patient Image"
                     style="object-fit: cover">
                <div class="image-caption">Patient Profile Image</div>
            </div>
        </div>"""

info_with_image = f"""
                <div style="
                display:flex;
                flex-direction: row;
                justify-content: space-between; 
                width: 100%;">
                {pateint_info}
                {image_html}
                </div>
                """
prediction_probs = {
    "Healthy": "14.90%",
    "URTI": "14.63%",
    "Asthma & Lung Fibrosis": "10.61%",
    "Pneumonia": "10.19%",
    "Heart Failure": "6.68%",
    "Heart Failure & Lung Fibrosis": "5.62%",
    "Bronchiolitis": "5.52%",
    "Pleural Effusion": "5.16%",
    "Bronchitis": "5.09%",
    "Lung Fibrosis": "4.89%",
    "LRTI": "3.94%",
    "Asthma": "3.70%",
    "Heart Failure & COPD": "3.38%",
    "COPD": "2.95%",
    "Bronchiectasis": "2.73%"
}

primary_condition, primary_value = list(prediction_probs.items())[0]
secondary_conditions = list(prediction_probs.items())[1:]

st.set_page_config(page_title="Medical Condition Prediction", layout="centered")

# Custom CSS styling
st.markdown("""
<style>
    
    .prediction-header {
        color: #2e86c1;
        font-size: 24px !important;
        font-weight: bold !important;
    }
    .patient-info {
        font-size: 24px;
        color: #566573;
        margin: 5px 0;
    }
    
    .image-container {
        border: 2px solid #2e86c1;
        border-radius: 8px;
        padding: 0;
        width: 154px;
        height: 184px;
        display: inline-block;
        overflow: hidden;
        margin-top: 25px;
    }
    .image-content {
        width: 150px;
        height: 180px;
        display: flex;
        flex-direction: column;
        align-items: center;
        margin: 2px;
    }
    .image-container img {
        width: 146px;
        height: 146px;
        object-fit: cover;
        border-radius: 5px;
        margin: 2px;  
    }
    .image-caption {
        color: #2e86c1;
        font-size: 14px;
        padding: 4px;
        text-align: center;
        width: 100%;
        border-top: 1px solid #2e86c1;
    }
</style>
""", unsafe_allow_html=True)

# Main header
st.header("respiratory diseases Prediction".title())


# Patient Information Row with Image
st.markdown("### Patient Information")
st.markdown(info_with_image, unsafe_allow_html=True)

# Prediction Results Section
st.markdown("### Prediction Results")
with st.container(): 
    st.markdown('<div class="prediction-card-marker"></div>', unsafe_allow_html=True)

    # Primary Prediction
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Primary Prediction", value=primary_value, delta="Highest Probability")
    with col2:
        st.markdown(f'<p class="prediction-header">{primary_condition}</p>', unsafe_allow_html=True)
        # Convert percentage string to float in 0–1 range
        st.progress(float(primary_value.strip('%')) / 100)


    # Divider
    st.markdown("---")

    # Secondary Predictions Grid
    st.markdown("**Other Potential Conditions**")
    rows = [secondary_conditions[i:i+3] for i in range(0, len(secondary_conditions), 3)]
    for row in rows:
        cols = st.columns(3)  # Always create 3 columns
        for i in range(3):
            if i < len(row):
                cond, val = row[i]
                cols[i].metric(label=f"{cond} Risk", value=val)
            else:
                cols[i].empty()  # Fill in with blank to maintain alignment
    
    

# Health Summary Dropdown
st.subheader("AI Summary and ChatBot")
with st.expander("View Health Summary", expanded=False):
     st.markdown(f"""
    <div style="background-color: #f8d7da; 
                padding: 20px; 
                border-radius: 10px;
                border-left: 4px solid #dc3545;
                margin: 10px 0;">
        <h4 style="color: #dc3545; margin-top: 0;">Key Risk Factors:</h4>
        <p style="color: #721c24; margin-bottom: 0;">
            <strong>Overall Risk Assessment:</strong> {summary}.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Spacer
st.markdown("<br>", unsafe_allow_html=True)