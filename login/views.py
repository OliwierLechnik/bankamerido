from django.shortcuts import render
from .forms import NewUser
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm


# Create your views here.
def login_view(req):
    form = AuthenticationForm(req.POST or None)
    if form.is_valid():
        cleaned = form.cleaned_data
        username = cleaned.get['username']
        passwd = cleaned.get['password']
    data = {
        'akcja': 'logowanie'
    }
    return render(req, 'login.html', data)


def register_view(req):
    form = NewUser(req.POST or None)
    if form.is_valid():
        form.save()
    else:
        print(form.errors)
    data = {
        'akcja': 'rejestracja',
        'form': form
    }
    return render(req, 'login.html', data)