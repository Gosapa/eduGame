from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', views.profile, name='profile'),
    path('save_achievement/', views.save_achievement, name="save_achievement"),
    path('delete_achievement/', views.delete_achievement, name='delete_achievement'),
    path('friends/', views.list_friends, name="friends"),
    path('friends/add/<int:user_id>/', views.send_friend_request, name="friend_request"),
    path('friends/requests/', views.list_received_request, name="received_friend_request"),
    path('friends/accept/<int:requestID>/', views.accept_friend_request, name="accept_friend_request"),
    path('friends/reject/<int:requestID>/', views.reject_friend_request, name="reject_friend_request"),
    path('friends/remove/<int:friendID>/', views.remove_friend, name="remove_friend"),
]
