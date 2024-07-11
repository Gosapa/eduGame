from . import config, prompts
import json

def gemini_generate_question(subject, details):
    model = config.question_model
    prompt = prompts.prompt_generate_questions(subject,details)
    raw_response = model.generate_content(prompt)
    response = json.loads(raw_response.text)
    print(response)
    return response