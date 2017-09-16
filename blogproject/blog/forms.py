from django import forms

from .models import Post

class PublishForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'title',
            'body',
            'category',
            'tags',
        ]

