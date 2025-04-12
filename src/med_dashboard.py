import streamlit as st
from google import genai
import os

# Replace with your API key
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
  Give a summary of the above repository predictions in a way a patient with no medical knowledge can understand. The probabilities are a probability distribution from the AI model
"""

client = genai.Client(api_key=Key)
response = client.models.generate_content(
    model="gemma-3-27b-it", contents=input_message
)
summary = response.text

# Data
patient = {"Name": "Susan Smith", "Age": 27, "Gender": "Female", "BMI": 29.7}
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

# Configure page
st.set_page_config(page_title="Medical Condition Prediction", layout="centered")

# Custom CSS Styling
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
</style>
""", unsafe_allow_html=True)

# Main header
st.header("Respiratory Diseases Prediction")

# Patient Information Row with Image (using st.columns for layout)
st.markdown("### Patient Information")
col1, col2 = st.columns([2, 1])
with col1:
    for key, value in patient.items():
        st.markdown(f"<div class='patient-info'>{key}: {value}</div>", unsafe_allow_html=True)
with col2:
    # Display the patient image using st.image (ensure the image file is in the correct path)
    st.image("../patient-pic.jpeg", caption="Patient Profile Image", width=150)

# Prediction Results Section
st.markdown("### Prediction Results")
with st.container():
    # Primary Prediction display
    col1, col2 = st.columns([1, 2])
    with col1:
        st.metric(label="Primary Prediction", value=primary_value, delta="Highest Probability")
    with col2:
        st.markdown(f'<p class="prediction-header">{primary_condition}</p>', unsafe_allow_html=True)
        # Convert percentage string to float in the 0–1 range for progress bar
        st.progress(float(primary_value.strip('%')) / 100)
    
    # Divider
    st.markdown("---")
    
    # Secondary Predictions Grid
    st.markdown("**Other Potential Conditions**")
    rows = [secondary_conditions[i:i+3] for i in range(0, len(secondary_conditions), 3)]
    for row in rows:
        cols = st.columns(3)  # Always create 3 columns for alignment
        for i in range(3):
            if i < len(row):
                cond, val = row[i]
                cols[i].metric(label=f"{cond} Risk", value=val)
            else:
                cols[i].empty()

# Health Summary Dropdown
st.subheader("AI Summary")
with st.expander("View Health Summary", expanded=False):
    st.markdown(f"""
    <div style="background-color: #f8d7da; 
                padding: 20px; 
                border-radius: 10px;
                border-left: 4px solid #dc3545;
                margin: 10px 0;">
        <h4 style="color: #dc3545; margin-top: 0;">Key Risk Factors:</h4>
        <p style="color: #721c24; margin-bottom: 0;">
            <strong>Overall Risk Assessment:</strong> {summary.strip()}
        </p>
    </div>
    """, unsafe_allow_html=True)

# Chatbot Interface Section
st.subheader("Chat with our AI Chatbot")

# Initialize chat history in session state if not already present
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input area
chat_input = st.text_input("Enter your message:", key="chat_input")
if st.button("Send"):
    if chat_input:
        with st.spinner("Loading response..."):
            pre_prompt = f"You are a model that will analyse some data returned from an ai audio prediction model for respiratory diseases. This is a summary of data from an LLM ( {summary.strip()} )that is displayed to user and here is model prediction data ({input_message}). Give helpful insight to the follow messag from user: "
            # Append the user's message to the chat history
            st.session_state.chat_history.append(("User",chat_input))
            # Use the Google chatbot model to generate a response
            chat_response = client.models.generate_content(
                model="gemma-3-27b-it",
                contents=pre_prompt+chat_input
            )
            bot_response = chat_response.text
            st.session_state.chat_history.append(("Bot", bot_response))

# Display the conversation
for sender, message in st.session_state.chat_history:
    if sender == "User":
        st.markdown(f"**You:** {message}")
    else:
        st.markdown(f"**Bot:** {message}")

# Spacer at the end
st.markdown("<br>", unsafe_allow_html=True)