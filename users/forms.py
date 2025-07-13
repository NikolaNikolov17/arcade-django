from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    profile_pic = forms.URLField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'profile_pic', 'password1', 'password2']