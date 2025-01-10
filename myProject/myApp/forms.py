from django.forms import ModelForm
from .models import Post, Genre, Comment
from django import forms


class PostForm(ModelForm):
    genres = forms.ModelMultipleChoiceField(queryset=Genre.objects.all(), widget=forms.CheckboxSelectMultiple)
    class Meta:
        model = Post
        fields = ['title', 'content', 'genres']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']