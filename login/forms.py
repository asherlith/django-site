from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import profile


class registrationform(UserCreationForm):
    email=forms.EmailField()
    class Meta:
        model=User
        fields=["username","email","password1","password2"]

class UserUpdateform(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]

class UpdateProfileform(forms.ModelForm):
    class Meta:
        model = profile
        fields = ["image"]

