from django.urls import path, include
from . import views

app_name = 'game'

urlpatterns = [
    path('start/', views.start_game, name='start_game'),
    path('load/<int:game_id>', views.load_game, name='load_game'),
    path('generate/<int:game_id>', views.generate_questions, name='generate_questions')
]
