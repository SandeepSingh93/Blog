from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField

class Article(models.Model):
    title = models.CharField(max_length=70)
    body = models.TextField()
    owner = models.ForeignKey(User)
    comment_count= models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)


class Comment(models.Model):
    article = models.ForeignKey(Article)
    content = models.TextField()
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    path = ArrayField(models.IntegerField(blank=True, editable=False))
    depth = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return str(self.content)
