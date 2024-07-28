from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from gemini.functions import gemini_generate_achievement
from .models import Achievement, Profile
import json

# Create your views here.


@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)

    achievements = Achievement.objects.filter(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile, 'achievements': achievements})

@login_required
def save_achievement(request):
    if request.method == "POST":
        user = request.user
        achievement = Achievement()
        data = json.loads(request.body)
        achievement.name = data['name']
        achievement.description = data['description']
        achievement.user = user
        achievement.save()
        return JsonResponse({"message": "successfully saved achievement"}, status=200)
    else:
        return JsonResponse({"message": "Invalid Request Method"}, status=400)
    

@login_required
def delete_achievement(request):
    if request.method == 'POST':
        achievement_id = request.GET.get('achievement_id')
        try:
            achievement = Achievement.objects.get(pk=achievement_id)
            achievement.delete()
            return JsonResponse({'success': True})
        except Achievement.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Achievement not found.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})