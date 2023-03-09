from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.contrib.auth import get_user_model
from .models import Account
from .forms import AccountCreationForm
from book.models import Book
from django.contrib.auth.models import User
from datetime import datetime
# Create your views here.


def account_picker_view(req):
    if not req.user.is_authenticated:
        return redirect('/')

    querry = Account.objects.filter(owner = req.user.username, active=True)
    off = Account.objects.filter(owner = req.user.username, active=False)

    data = {
        'user': req.user,
        'name': f'{req.user.first_name} {req.user.last_name}',
        'accs': querry,
        'waiting': off,
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
    return render(req, 'newAcc.html', data)


def account_detailed_view(req, acc_id):
    if not req.user.is_authenticated:
        return redirect('/')
    acc = get_object_or_404(Account, id=acc_id)
    if not acc.owner == req.user.username:
        return redirect('/')
    if not acc.active:
        return redirect('/')

    # history
    outgoing = Book.objects.filter(sender_id = acc_id)
    incoming = Book.objects.filter(receiver_id = acc.id)

    history = []
    for transfer in incoming:
        target = Account.objects.get(id = transfer.sender_id)
        user = User.objects.get(username = target.owner)
        subtitle = f'{user.first_name} {user.last_name} - {target.name}'
        history.append(
            {
                'title': transfer.title,
                'subtitle': subtitle,
                'date': datetime.strftime(transfer.date, '%d-%m-%Y'),
                'value': f'<p class="in">{transfer.value}A</p>',
                'id': transfer.id
            }
        )

    for transfer in outgoing:
        target = Account.objects.get(id = transfer.receiver_id)
        user = User.objects.get(username = target.owner)
        subtitle = f'{user.first_name} {user.last_name} - {target.name}'
        history.append(
            {
                'title': transfer.title,
                'subtitle': subtitle,
                'date': datetime.strftime(transfer.date, '%d-%m-%Y'),
                'value': f'<p class="out">-{transfer.value}A</p>',
                'id': transfer.id
            }
        )

    history = sorted(history, key = lambda x: x.get('id'), reverse=True)

    options = {

    }

    super_options = {

    }

    data = {
        'acc': acc,
        'name': f'{req.user.first_name} {req.user.last_name} - {acc.name}',
        'history': history
    }
    return render(req, 'detailed.html', data)




