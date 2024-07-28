from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import GameForm
from .models import Game
from gemini.functions import gemini_generate_question, gemini_generate_achievement
from django.contrib.auth.decorators import login_required
from users.models import Profile

# Create your views here.

@login_required
def start_game(request):
    form = GameForm(request.POST or None)
    if form.is_valid():
        game = form.save(commit=False)
        game.user = request.user
        game.save()
        return redirect('game:load_game', game_id = game.id)
    return render(request, 'game/start_game.html', {'form': form})

@login_required
def load_game(request, game_id):
    return render(request, 'game/game_loading.html', {'game_id': game_id})

@login_required
def generate_questions(request, game_id):
    game = Game.objects.get(id=game_id)
    # print(game.subject)
    # print(game.details)
    response = gemini_generate_question(game.subject, game.details)
    game.questions = response
    game.save()
    # print(game.questions)
    # print(type(game.questions))
    return JsonResponse({'message': f'successfully generated questions for game {game_id}'}, status=200)
    
@login_required
def play_game(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request,'game/play_game.html', {'game': game})

@login_required
def end_game(request, game_id):
    if request.method == "POST":
        user = request.user
        game = Game.objects.get(id=game_id)
        profile = Profile.objects.get(user=user)
        profile.games_completed += 1
        session_title = game.subject + "(" + game.details + ")"
        profile.subjects_completed[session_title] = profile.subjects_completed.get(session_title, 0) + 1
        profile.save()

        score = 0
        question = game.questions
        tmpgrade = []
        for i in range(len(question)):
            if request.POST.get(str(i)) == question[i]["correct_answer"]:
                score += 1
                tmpgrade.append(1)
            else:
                tmpgrade.append(0)
        game.score = score
        game.grade = tmpgrade
        game.save()
        achievement = gemini_generate_achievement(user,game_id)
        return render(request, 'game/end_game.html', {'achievement': achievement, 'game': game})
    else:
        return JsonResponse({"message": "Invalid Request Method"}, status=400)

@login_required
def list_game(request):
    games = Game.objects.filter(user=request.user)
    return render(request, 'game/game_list.html', {'games': games})

@login_required
def delete_game(request):
    if request.method == 'POST':
        game_id = request.GET.get('game_id')
        try:
            game = Game.objects.get(pk=game_id)
            game.delete()
            return JsonResponse({'success': True})
        except Game.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'game not found.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})