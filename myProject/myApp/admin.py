from django.contrib import admin

# Register your models here.
from .models import Post, Comment, Genre
from .views import category

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Genre)