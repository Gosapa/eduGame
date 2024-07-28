from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Game(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    subject = models.CharField(max_length=100)
    details = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)
    questions = models.JSONField(default=list)
    score = models.IntegerField(default=-1)
    grade = models.JSONField(default=list)

    def __str__(self):
        return f'{self.subject}: {self.details} - {self.user.username}'
    
    class Meta:
        ordering = ['-date_created']