from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialAccount
from gemini.functions import gemini_generate_achievement
from .models import Achievement, Profile, Friend_Request
from django.contrib.auth import get_user_model
import json

User = get_user_model()

# Create your views here.


@login_required
def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    profile = Profile.objects.get(user=user)
    achievements = Achievement.objects.filter(user=user)
    return render(request, 'users/profile.html', {'profile': profile, 'achievements': achievements, "profile_user": user})

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
    


@login_required
def list_friends(request):
    friends = request.user.friends.all()
    return render(request, 'users/friends.html', {'friends': friends})

@login_required
def send_friend_request(request, user_id):
    from_user = request.user
    to_user = User.objects.get(id=user_id)
    if from_user == to_user:
        return HttpResponse('You cannot send a friend request to yourself.') 
    if to_user in from_user.friends.all():
        return HttpResponse('You are already friends with this user.' )
    friend_request, created = Friend_Request.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('Friend request sent!')
    else:
        return HttpResponse('Friend request already sent!')
    
@login_required
def list_received_request(request):
    currentUser = request.user
    received_requests = Friend_Request.objects.filter(to_user=currentUser)
    return render(request,'users/friend_requests.html', {'friendrequests': received_requests})

@login_required
def accept_friend_request(request, requestID):
    friend_request = Friend_Request.objects.get(id=requestID)
    if friend_request.to_user == request.user:
        friend_request.to_user.friends.add(friend_request.from_user)
        friend_request.from_user.friends.add(friend_request.to_user)
        friend_request.delete()
        return HttpResponse('friend request accepted')
    else:
        return HttpResponse('Invalid Request')

@login_required
def reject_friend_request(request, requestID):
    if request.method == 'POST':
        try:
            friend_request = Friend_Request.objects.get(id=requestID)
            friend_request.delete()
            return JsonResponse({'success': True})
        except Friend_Request.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Friend request not found.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})
    
@login_required
def remove_friend(request, friendID):
    if request.method == 'POST':
        try:
            friend = User.objects.get(id=friendID)
            request.user.friends.remove(friend)  # Remove friend from current user's list
            friend.friends.remove(request.user)  # Remove current user from friend's list
            return JsonResponse({'success': True})
        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Friend not found.'})
    else:
        return JsonResponse({'success': False, 'error': 'Invalid request method.'})