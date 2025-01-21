from django.forms import TextInput, ModelForm
from .models import Post, Comment, Profile
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

class AvatarUploadForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar']

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar')
        if avatar:
            if avatar.size > 10485760:  # 10 MB
                raise forms.ValidationError("Avatar file size must be under 10 MB")
            if not avatar.content_type in ['image/jpeg', 'image/png']:
                raise forms.ValidationError("Avatar file must be a JPEG or PNG image")
        return avatar