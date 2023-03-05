from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
# Create your views here.


def account_home_view(req):
    if not req.user.is_authenticated:
        return redirect('../')
    data = {
        'user': req.user
    }
    return render(req, 'home.html', data)





