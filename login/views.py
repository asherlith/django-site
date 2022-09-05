from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import registrationform, UserUpdateform, UpdateProfileform


def register(request):
    if request.method == "POST":
        form = registrationform(request.POST)
        if form.is_valid():
            form.save()
            #username = form.cleaned_data.get("username")
            messages.success(request, "user created successfully")
            return redirect("login")
    else:
        form = registrationform()
    return render(request, "registration.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        user_form = UserUpdateform(request.POST, instance=request.user)
        profile_form = UpdateProfileform(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, "updated successfully")
            return redirect("page-home")

    else:
        user_form = UserUpdateform(instance=request.user)
        profile_form = UpdateProfileform(instance=request.user.profile)
    context = {
        "user_form": user_form,
        "profile_form": profile_form
    }
    return render(request, "profile.html", context)
