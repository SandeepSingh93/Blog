from django.forms import ModelForm
from blog.models import *

class article_form(ModelForm):
    class Meta:
        model= Article
        fields= ('title', 'body', )