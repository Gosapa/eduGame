import json
from users.models import Profile, Achievement
from game.models import Game
from django.contrib.auth import get_user_model
User = get_user_model()

def prompt_generate_questions(subject, details):
    return f"""Please create 10 multiple choice questions about {subject}, on {details}
format: list[question]
question: {{'question': 'GENERATED QUESTION', 'answer_choices': {{ 'a': 'GENERATED ANSWER CHOICE' , 'b' ... 'd'}}, 'correct_answer': 'CORRECT ANSWER FOR YOUR QUESTION'}}
"""

def prompt_generate_achievement2(user):
    profile = Profile.objects.get(user=user)
    achievements = Achievement.objects.filter(user=user)
    achievement_names = ""
    for achievement in achievements:
        achievement_names += achievement.name + "\n"

    return f"""
If you think user deserves an achievement (example: 100th game completed, studied same subject 10 times, etc.), create an appropriate name of an achievement for our education game, where users can answer ai-generated questions about various subjects to learn about them.
You can also choose not to generate achievement, as users would have too many achievements if user receives an achievement every time they finish a game.
This message is sent after a user finishes a study game session.
Please create an achievement when user finished their first game (when the number of completed games is 1).
You can create creative and fun names, but please don't make them overlapping.

user data:
total games completed: { profile.games_completed }
subjects completed (key=name of subject, value=number of games completed): { json.dumps(profile.subjects_completed) }

achievements:
{achievement_names}
output format: dict
{{'created': '0 OR 1, 0 IF NO ACHIEVEMENT CREATE, 1 IF CREATED, 'name': 'EMPTY IF NO ACHIEVEMENT CREATED, NAME OF ACHIEVEMENT IF CREATED'}}
"""
def prompt_generate_achievement(user, game_id):
    profile = Profile.objects.get(user=user)
    achievements = Achievement.objects.filter(user=user)
    achievement_names = ""
    game = Game.objects.get(id=game_id)
    for achievement in achievements:
        achievement_names += achievement.name +": " + achievement.description + "\n"

    return f"""
Create an creative name of an achievement for the following user!
just completed a game of {game.subject}({game.details}) with score of {game.score}/10.
user data:
total games completed: { profile.games_completed }
subjects completed (key=name of subject, value=number of games completed): { json.dumps(profile.subjects_completed) }
achievements:
{achievement_names}
Please create a creative and fun names of the user!
Also, please generate output in a json format:
{{'name': 'NAME OF ACHIEVEMENT', 'description': 'DESCRIPTION OF ACHIEVEMENT'}}
"""