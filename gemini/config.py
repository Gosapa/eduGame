import google.generativeai as genai

GOOGLE_AI_KEY = "AIzaSyAXRo1Z0Qs63t18ZQiyuMOLWXkBeKezSd0"

genai.configure(api_key=GOOGLE_AI_KEY)

question_model = genai.GenerativeModel("gemini-1.5-flash-latest",
                                       system_instruction="You are an AI that creates problem sets with given subjects for educational purposes for students.",
                                       generation_config={"response_mime_type": "application/json"})