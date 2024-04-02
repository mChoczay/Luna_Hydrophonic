from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django import forms

# - Create/Register an user


class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ["username", "password1", "password2"]


# - Login an user


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
