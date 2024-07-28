import google.generativeai as genai
from edugame.settings import GOOGLE_AI_KEY

genai.configure(api_key=GOOGLE_AI_KEY)

question_model = genai.GenerativeModel("gemini-1.5-flash-latest",
                                       system_instruction="You are an AI that creates problem sets with given subjects for educational purposes for students.",
                                       generation_config={"response_mime_type": "application/json"})
achievement_model = genai.GenerativeModel("gemini-1.5-flash-latest",
                                       system_instruction="You are an AI that creates name of achievements according to the given user data, in our education game.",
                                       generation_config={"response_mime_type": "application/json"})
