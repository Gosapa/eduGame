from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.



class Achievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300, default="")
    date_created = models.DateTimeField(auto_now_add=True)

class Profile(models.Model):
    # add user
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=1)
    games_completed = models.IntegerField(default=0)
    subjects_completed = models.JSONField(default=dict, null=True)
    
    def __str__(self):
        return self.user.username
    