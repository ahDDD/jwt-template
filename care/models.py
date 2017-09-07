from django.db import models
from account.models import User


class Post(models.Model):
    title = models.CharField(max_length=40)
    detail = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    user = models.ForeignKey('问询的所属用户', to=User, related_name='question')
    doctor = models.ForeignKey('问询的所属医生', to=User, related_name='answer')


class Comment(models.Model):
    post = models.ForeignKey('对应的问询', to=Post, related_name='comment')
    content = models.TextField()
    user = models.ForeignKey('回复的用户或医生', to=User, related_name='reply')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
