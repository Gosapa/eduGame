
def prompt_generate_questions(subject, details):
    return f"""Please create 10 multiple choice questions about {subject}, on {details}
format: list[question]
question: {{'question': 'GENERATED QUESTION', 'answer_choices': {{ 'a': 'GENERATED ANSWER CHOICE' , 'b' ... 'd'}}, 'correct_answer': 'CORRECT ANSWER FOR YOUR QUESTION'}}
"""