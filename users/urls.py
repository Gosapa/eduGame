from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    path('save_achievement/', views.save_achievement, name="save_achievement"),
    path('delete_achievement/', views.delete_achievement, name='delete_achievement'),
]
