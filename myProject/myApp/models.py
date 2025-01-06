from django.db import models
from django.contrib.auth.models import User
from django.db.models import SET_NULL


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=50)
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(null=False, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    genre = models.ForeignKey('Genre', on_delete=SET_NULL, null=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post')
    content = models.TextField(null=False)
    author_name = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

class Genre(models.Model):
    name = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name