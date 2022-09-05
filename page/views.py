from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import post, UserFollowing, Comment, songs
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from .forms import AddComment
from django.contrib.auth.models import User


class Listexplore(ListView):
    model = post
    template_name = "explore.html"
    context_object_name = "post"
    ordering = ["-time"]
    paginate_by = 10

    def post(self, request, **kwargs):
        form = AddComment(request.POST)
        if form.is_valid():
            form.instance.post = post.objects.get(pk=request.POST["pk"])
            form.instance.user = self.request.user
            if request.POST.get("parent") is not None:
                form.instance.parent = Comment.objects.get(id=request.POST.get("parent"))
            form.save()
        else:
            messages.error(self.request, form.errors)
        return redirect(request.META['HTTP_REFERER'])

    def get_context_data(self, **kwargs):
        context = super(Listexplore, self).get_context_data(**kwargs)
        context["user_form"] = AddComment()
        return context


class Listhome(LoginRequiredMixin, ListView):
    model = post
    template_name = "home.html"
    context_object_name = "post"
    ordering = ["-time"]
    paginate_by = 10

    def post(self, request, **kwargs):
        form = AddComment(request.POST)
        if form.is_valid():
            form.instance.post = post.objects.get(pk=request.POST["pk"])
            form.instance.user = self.request.user
            if request.POST.get("parent") is not None:
                form.instance.parent = Comment.objects.get(id=request.POST.get("parent"))
            form.save()
        else:
            messages.error(self.request, form.errors)
        return redirect(request.META['HTTP_REFERER'])

    def get_queryset(self):
        set0 = [self.request.user]
        set1 = list(UserFollowing.objects.filter(user=self.request.user).values_list("following_user")) + set0
        return post.objects.filter(author__in=set1).order_by("-time")

    def get_context_data(self, **kwargs):
        context = super(Listhome, self).get_context_data(**kwargs)
        context["form"] = AddComment()
        return context


class DetailPost(DetailView):
    model = post
    template_name = "post_detail.html"


class CreatePost(LoginRequiredMixin, CreateView):
    model = post
    fields = ["title", "caption", "music", "media"]
    template_name = "post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)


class UpdatePost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = post
    fields = ["title", "caption", "music", "media"]
    template_name = "post_update.html"

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, form.errors)
        return super().form_invalid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = post
    template_name = "post_delete.html"
    success_url = "http://127.0.0.1:8000/home/"

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class UserList(ListView):
    model = post
    template_name = "user_posts.html"
    context_object_name = "post"
    paginate_by = 10

    def post(self, request, **kwargs):
        user2 = get_object_or_404(User, username=self.kwargs.get("username"))

        try:
            UserFollowing.objects.get(following_user=user2, user=request.user)
            created = UserFollowing.objects.get(following_user=user2, user=request.user)
            created.delete()
            request.user.profile.follower -= 1
            user2.profile.following -= 1
            request.user.save()
            user2.save()

        except UserFollowing.DoesNotExist:
            created = UserFollowing.objects.create(following_user=user2, user=request.user)
            request.user.profile.follower += 1
            user2.profile.following += 1
            created.save()
            request.user.save()
            user2.save()

        return redirect(request.META['HTTP_REFERER'])

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return post.objects.filter(author=user).order_by("-time")

    def get_context_data(self, **kwargs):
        context = super(UserList, self).get_context_data(**kwargs)
        context['user2'] = get_object_or_404(User, username=self.kwargs.get("username"))
        my_user = User.objects.get(username=self.request.user.username)
        try:
            UserFollowing.objects.get(following_user=context['user2'], user=my_user)
            follow = True
        except UserFollowing.DoesNotExist:
            follow = False

        context['follow'] = follow
        return context


class Follow(ListView):
    model = UserFollowing
    template_name = "user_follow_detail.html"
    context_object_name = "follow"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return UserFollowing.objects.filter(following_user=user)


class Following(ListView):
    model = UserFollowing
    template_name = "user_following_detail.html"
    context_object_name = "following"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        print(UserFollowing.objects.filter(user=user))
        return UserFollowing.objects.filter(user=user)


def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        obj = User.objects.filter(username__contains=searched)
        return render(request, "search_results.html", context={"searched": searched,
                                                               "obj": obj
                                                               })
    else:
        return render(request, "search_results.html", {})


def tags(request, tags):
    tags = '#' + tags
    tag_posts = post.objects.filter(caption__icontains=tags).order_by('-time')
    return render(request, 'tags.html', {'post': tag_posts})


def music_player(request):
    context = songs.objects.all()
    return render(request, 'music_player.html', context={"songs": context})


def search_music(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        song_name = songs.objects.filter(name__contains=searched)
        song_singer = songs.objects.filter(singer__contains=searched)
        return render(request, "search_results_music.html", context={"searched": searched,
                                                                     "song_name": song_name,
                                                                     "song_singer": song_singer
                                                                     })
    else:
        return render(request, "search_results_music.html", {})


def about(request):
    return render(request, "about.html")


def test(request):
    return render(request, "tests.html")
