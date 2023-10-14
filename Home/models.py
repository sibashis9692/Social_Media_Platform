from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=5)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = userManager()


class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    friends = models.ManyToManyField(User, related_name='user_connections')




class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    images = models.ImageField('images/')
    time = models.DateTimeField(auto_now_add=True)
    caption = models.TextField()
    is_liked = models.BooleanField(default=False)
    is_comment = models.BooleanField(default=False)
    likes = models.IntegerField()
    comments = models.IntegerField()
    comment = models.TextField()
