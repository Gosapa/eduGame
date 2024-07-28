from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up  # Import allauth signal
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import Profile

@receiver(user_signed_up)  # Use allauth's user_signed_up signal
def create_user_profile(request, user, **kwargs):
    """Creates a default Profile when a new user signs up via allauth."""
    if kwargs.get('sociallogin').account.provider == 'google':  # Check if Google login
        Profile.objects.create(user=user) 