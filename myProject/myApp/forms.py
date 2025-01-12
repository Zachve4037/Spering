from django.forms import TextInput, ModelForm
from .models import Post, Genre, Comment
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'genres']
        widgets = {
            'title': TextInput(attrs={'class': 'form-control',
                                      'style': 'max-width:  500px;',
                                      'placeholder': 'Title'}),
            'content': forms.Textarea(attrs={'class': 'form-control',
                                             'style': 'max-width: 500px;',
                                             'placeholder': 'Content'}),
            'genres': forms.CheckboxSelectMultiple(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={'class': 'form-control',
                                              'style': 'max-width: 500px;',
                                              'placeholder': 'Content'}),
        }
