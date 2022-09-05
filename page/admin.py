from django.contrib import admin
from .models import post, songs, UserFollowing, Comment

admin.site.register(songs)
admin.site.register(post)
admin.site.register(UserFollowing)
admin.site.register(Comment)

# Register your models here.
