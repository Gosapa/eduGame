from django.db import models

# Create your models here.

class Game(models.Model):
    subject = models.CharField(max_length=100)
    details = models.CharField(max_length=200)
    date_created = models.DateTimeField(auto_now_add=True)