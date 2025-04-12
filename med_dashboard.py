import streamlit as st
import pandas as pd


#TODO  
# Add functionality to upload or record audio recording for processing
# Add loading bar to emulate api call to model

#Data 
HEALTH_SUMMARY_DATA = {
    "⚠️ Blood Pressure": "180/110 mmHg (Stage 2 Hypertension)",
    "❗ Cholesterol": "240 mg/dL (Elevated)",
    "📈 Blood Sugar": "140 mg/dL (High)",
    "⚖️ BMI": "29.7 (Overweight)",
    "👪 Family History": "Hypertension"
}
table_rows = "".join(
        f"""<tr>
            <td style='padding: 8px 0;'>{key}</td>
            <td style='padding: 8px 0;'>{value}</td>
        </tr>""" 
        for key, value in HEALTH_SUMMARY_DATA.items()
    )

patient = {"Name": "John Doe","Age":58,"Gender": "Male","BMI":29.7}
pateint_info = "".join(
    f"""<div class="patient-info">{key}: {value}</div>"""
    for key,value in patient.items()
)




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
patient_col, image_col = st.columns([3, 1])
with patient_col:
    st.markdown("### Patient Information")
    st.markdown(pateint_info, unsafe_allow_html=True)

with image_col:
    try:
        st.markdown('''
        <div class="image-container">
            <div class="image-content">
                <img src="./patient-pic.jpeg" 
                     alt="Patient Image"
                     style="object-fit: cover">
                <div class="image-caption">Patient Profile Image</div>
            </div>
        </div>
        ''', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("Patient image not found! Please check the file path.")

# Prediction Results Section
st.markdown("### Prediction Results")
with st.container(): 
    st.markdown('<div class="prediction-card-marker"></div>', unsafe_allow_html=True)
    
    # Primary Prediction
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Primary Risk", value="65%", delta="High Risk")
    with col2:
        st.markdown('<p class="prediction-header">Hypertension</p>', unsafe_allow_html=True)
        st.progress(65)
    
    # Divider
    st.markdown("---")
    
    # Secondary Predictions Grid
    st.markdown("**Other Potential Conditions**")
    pred_col1, pred_col2, pred_col3 = st.columns(3)
    with pred_col1:
        st.metric(label="Diabetes Risk", value="20%", delta="Moderate")
    with pred_col2:
        st.metric(label="Heart Disease Risk", value="15%", delta="Low")
    with pred_col3:
        st.metric(label="Kidney Disease Risk", value="8%", delta="Low")
    
    

# Medical Record Table
st.subheader("Medical Record")
with st.expander("📁 Medical Record", expanded=False):
    medical_data = {
        "Clinical Parameter": [
            "Systolic Blood Pressure",
            "Diastolic Blood Pressure",
            "Cholesterol Level",
            "Blood Sugar Level",
            "Family History"
        ],
        "Measurement": [
            "180 mmHg",
            "110 mmHg",
            "240 mg/dL",
            "140 mg/dL",
            "Hypertension"
        ]
    }

    df = pd.DataFrame(medical_data)
    st.dataframe(
        df,
        hide_index=True,
        use_container_width=True,
        column_config={
            "Clinical Parameter": st.column_config.Column(width="large"),
            "Measurement": st.column_config.Column(width="medium")
        }
    )


# Health Summary Dropdown
with st.expander("View Health Summary", expanded=False):
     st.markdown(f"""
    <div style="background-color: #f8d7da; 
                padding: 20px; 
                border-radius: 10px;
                border-left: 4px solid #dc3545;
                margin: 10px 0;">
        <h4 style="color: #dc3545; margin-top: 0;">Key Risk Factors:</h4>
        <table style="width: 100%; color: #721c24; margin-bottom: 15px;">
            {table_rows}
        </table>
        <p style="color: #721c24; margin-bottom: 0;">
            <strong>Overall Risk Assessment:</strong> High cardiovascular risk profile 
            requiring immediate lifestyle modifications and clinical monitoring.
        </p>
    </div>
    """, unsafe_allow_html=True)


# Spacer
st.markdown("<br>", unsafe_allow_html=True)