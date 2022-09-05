from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django import forms


class songs(models.Model):
    name = models.CharField(max_length=30)
    song = models.FileField()
    singer = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    time = models.DateTimeField(auto_now_add=True)
    media = models.FileField()
    music = models.ForeignKey(songs, on_delete=models.CASCADE)
    caption = models.TextField()
    title = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name="following", on_delete=models.CASCADE)
    following_user = models.ForeignKey(User, related_name="followers", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(post, related_name="comment", on_delete=models.CASCADE)
    content = models.TextField()
    parent = models.ForeignKey('self', null=True,blank=True, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True