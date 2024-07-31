from django.db import models

from accounts.models import User


class Topic(models.Model):
    """ Topic base model"""
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=150, blank=False, null=False)
    content = models.CharField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.title


class Comment(models.Model):
    """ Comment base model """
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    content = models.TextField(max_length=500, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return self.content
