from django.contrib import admin
from blog.models import *



class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'title', 'body', 'created_at', 'updated_at')


admin.site.register(Article,ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'article', 'user', 'content', 'date', 'path', 'depth')


admin.site.register(Comment,CommentAdmin)