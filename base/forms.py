from django.forms import forms
from django.forms import ModelForm
from .models import Group, User
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'password1', 'password1']


class GroupForm(ModelForm):
    class Meta:
        model = Group
        fields = "__all__"
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name', 'username', 'email']
