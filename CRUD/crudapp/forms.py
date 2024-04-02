from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from .models import HydroponicSystem

# - Create/Register an user


class CreateUserForm(UserCreationForm):

    class Meta:

        model = User
        fields = ["username", "password1", "password2"]


# - Login an user


class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


# - Add a hydroponic system
    

class AddSystemForm(forms.ModelForm):
    class Meta:
        model = HydroponicSystem
        fields = ["name", "description", "ph", "water_temperature", "TDS"] #TODO swap to take data from db for ph, water_temperature, TDS


# - Update a hydroponic system
    

class UpdateSystemForm(forms.ModelForm):

    class Meta:
        model = HydroponicSystem
        fields = ["name", "description", "ph", "water_temperature", "TDS"]


