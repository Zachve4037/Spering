from django.forms import ModelForm
from .models import Post, Genre
from django import forms


class PostForm(ModelForm):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = ['title', 'content', 'genres']