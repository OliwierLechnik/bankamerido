from django.shortcuts import render, redirect
from .forms import NewUser, LoginForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages

# Create your views here.
def login_view(req):
    if req.user.is_authenticated:
        return redirect('home/')
    form = LoginForm(req, data=req.POST or None)
    data = {
        'akcja': 'Logowanie',
        'form': form,
        'text': 'Nie masz konta? <a href="register/">Załóż je!</a>'
    }
    if form.is_valid():
        cleaned = form.cleaned_data
        name = cleaned.get('username')
        passwd = cleaned.get('password')
        user = authenticate(username=name, password=passwd)
        if user is not None:
            login(req, user)
            print('suka')
            return redirect('home/')
    else:
        if not req.POST:
            form.error_messages = []


    if req.user.is_authenticated:
        return redirect('home/')
    return render(req, 'login.html', data)


def logout_view(req):
    if not req.user.is_authenticated:
        return redirect('../')
    logout(req)
    return redirect('../')

def register_view(req):
    if req.user.is_authenticated:
        return redirect('../home/')
    form = NewUser(req.POST or None)
    if form.is_valid():
        form.save()
        return redirect('../')
    data = {
        'akcja': 'Rejestracja',
        'form': form,
        'text': 'Masz konto? <a href="../">Zaloguj się!</a>'
    }
    return render(req, 'login.html', data)