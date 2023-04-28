from django import forms
from django.forms import ModelForm

from .models import Comment, Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'group': forms.Select(attrs={'class': 'form-control'})
        }


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Добавить комментарий'}
        help_texts = {'text': 'Текст нового комментария'}
