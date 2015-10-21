from django.contrib import admin
from blog.models import *


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'body', 'created_at', 'updated_at')
