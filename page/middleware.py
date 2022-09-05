from django.http.response import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse
from django.http import HttpRequest
from .models import User, UserFollowing


def follow_middleware(get_response):
    def middleware(request):

        if '/user/' in request.path_info:
            if request.path_info.find("/follow") == -1:
                username = request.path_info[6:-1]
                user2 = get_object_or_404(User, username=username)
                user2.profile.following = UserFollowing.objects.filter(following_user=user2).count()
                user2.profile.follower = UserFollowing.objects.filter(user=user2).count()
                user2.save()

        response = get_response(request)
        return response

    return middleware
