from django.db import models
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    sent = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    name = models.CharField(max_length=150)
    user = models.ManyToManyField(User)
