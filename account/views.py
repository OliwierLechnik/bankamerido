from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from .models import Account
from .forms import AccountCreationForm
# Create your views here.


def account_picker_view(req):
    if not req.user.is_authenticated:
        return redirect('/')

    querry = Account.objects.filter(owner = req.user.username, active=True)

    data = {
        'user': req.user,
        'accs': querry,
    }
    print(querry)
    return render(req, 'home.html', data)


def account_create_view(req):
    if not req.user.is_authenticated:
        return redirect('/')
    form = AccountCreationForm(req.POST or None)
    data = {
        'form': form,
    }
    if form.is_valid():
        acc = Account.objects.create(owner=req.user.username, name=form.cleaned_data.get('name'))
        return redirect('/account/')
    return render(req, 'new.html', data)


def account_detailed_view(req, acc_id):
    if not req.user.is_authenticated:
        return redirect('/')
    acc = get_object_or_404(Account, id=acc_id)
    if not acc.owner == req.user.username:
        return redirect('/')
    if not acc.active:
        return redirect('/')

    data = {
        'acc': acc,
    }
    return render(req, 'detailed.html', data)




