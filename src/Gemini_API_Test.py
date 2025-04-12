from google import genai
from dotenv import load_dotenv 
import os

load_dotenv()

def main():
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

    client = genai.Client(api_key=os.getenv("API_KEY"))
    response = client.models.generate_content(
        model="gemma-3-27b-it", contents=input_message
    )
    print(response.text)


if __name__ == "__main__":
    main()
