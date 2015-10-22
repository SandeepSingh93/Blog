from django import forms
from blog.models import *

class article_form(forms.ModelForm):
    class Meta:
        model= Article
        fields= ('title', 'body', )


class comment_form(forms.ModelForm):
    parent = forms.CharField(widget=forms.HiddenInput(
                            attrs={'class': 'parent'}), required=False)
    class Meta:
        model= Comment
        fields= ('content',)