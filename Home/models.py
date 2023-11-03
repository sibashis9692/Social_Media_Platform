from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import *


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=5)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = userManager()

    def __str__(self):
        return f"{self.username}"

class Connection(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    friends = models.ManyToManyField(User, related_name='user_connections')

    def __str__(self) -> str:
        return self.user.username
    

def upload_to(instance, filename):
    return filename.format(filename=filename)


class Posts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    images = models.ImageField(upload_to = upload_to)
    time = models.DateTimeField(auto_now_add=True)
    caption = models.TextField()
    total_likes = models.IntegerField(null=True, default=0, editable=False)
    total_comments = models.IntegerField(null=True, default=0, editable=False)
    my_comments = models.TextField()
    all_comments = models.URLField()

    def __str__(self) -> str:
        return self.user.username
    
class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comment = models.TextField()


class Likes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    like = models.BooleanField()