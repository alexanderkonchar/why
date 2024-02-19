from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Follower(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="people_you_follow")
    follows = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")


class Post(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    edited = models.BooleanField(default=False)
    likes = models.IntegerField(default=0)
