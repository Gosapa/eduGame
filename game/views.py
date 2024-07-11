from django.shortcuts import render, redirect
from django.http import JsonResponse
from .forms import GameForm
from .models import Game
from gemini.functions import gemini_generate_question
from django.contrib.auth.decorators import login_required

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
    print(game.subject)
    print(game.details)
    response = gemini_generate_question(game.subject, game.details)
    return JsonResponse({'message': f'successfully generated questions for game {game_id}'}, status=200)
    