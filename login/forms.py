from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Login',
            },
        )
    )
    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Hasło',
            },
        )
    )
    class Meta:
        model = User
        fields = [
            'username',
            'password',
        ]


class NewUser(UserCreationForm):
    username = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Login',
            },
        )
    )
    email = forms.EmailField(
        label='',
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Email',
            },
        )
    )
    first_name = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Imię',
            },
        )
    )
    last_name = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Nazwisko',
            },
        )
    )
    password1 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Hasło',
            },
        )
    )
    password2 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Potwierdź hasło',
            },
        )
    )
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
