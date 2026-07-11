import google.generativeai as genai
from config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")

def test_gemini_connection():
    response = model.generate_content("Say 'Gemini is connected' in one short sentence.")
    return response.text

if __name__ == "__main__":
    print(test_gemini_connection())
    