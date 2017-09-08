from django.db import models
from account.models import User


class Post(models.Model):
    title = models.CharField(max_length=40, null=False)
    detail = models.TextField(blank=True, null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, related_name='question')
    doctor = models.ForeignKey(to=User, related_name='answer')


class Comment(models.Model):
    post = models.ForeignKey(to=Post, related_name='comment')
    content = models.TextField()
    user = models.ForeignKey(to=User, related_name='reply')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
