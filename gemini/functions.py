from . import config, prompts
import json

def gemini_generate_question(subject, details):
    model = config.question_model
    prompt = prompts.prompt_generate_questions(subject,details)
    raw_response = model.generate_content(prompt)
    print(raw_response)
    response = json.loads(raw_response.text)
    # print(response)
    return response

def gemini_generate_achievement(user, game_id):
    model = config.achievement_model
    prompt = prompts.prompt_generate_achievement(user, game_id)
    print(prompt)
    raw_response = model.generate_content(prompt)
    response = json.loads(raw_response.text)
    return response