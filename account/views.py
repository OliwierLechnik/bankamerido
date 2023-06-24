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
        'super': req.user.is_superuser
    }
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

    slownik = {
        'regular_transfer': 'Przelew',
        'super_transfer': 'Super przelew',
        'deposit': 'Dodaj pieniądz',
        'withdraw': 'Usuń pieniądz',
        'debt_collection': 'Windykacja',
    }

    history = []
    for transfer in incoming:
        try:
            target = Account.objects.get(id = transfer.sender_id)
            user = User.objects.get(username = target.owner)
            subtitle = f'{user.first_name} {user.last_name} - {target.name}'
        except:
            subtitle = f'Konto usunięte id={transfer.sender_id}'
        history.append(
            {
                'title': transfer.title,
                'subtitle': subtitle,
                'date': datetime.strftime(transfer.date, '%d-%m-%Y'),
                'value': f'<p class="in">{transfer.value}A</p>',
                'id': transfer.id,
                'type': slownik.get(transfer.type)
            }
        )

    for transfer in outgoing:
        try:
            target = Account.objects.get(id = transfer.sender_id)
            user = User.objects.get(username = target.owner)
            subtitle = f'{user.first_name} {user.last_name} - {target.name}'
        except:
            subtitle = f'Konto usunięte id={transfer.sender_id}'
        history.append(
            {
                'title': transfer.title,
                'subtitle': subtitle,
                'date': datetime.strftime(transfer.date, '%d-%m-%Y'),
                'value': f'<p class="out">-{transfer.value}A</p>',
                'id': transfer.id,
                'type': slownik.get(transfer.type)
            }
        )

    history = sorted(history, key = lambda x: x.get('id'), reverse=True)

    opcje = [
        {
            'name': 'Przelew',
            'address': 'transfer/'
        },
    ]

    super_opcje = [
        {
            'name': 'Windykacja',
            'address': 'debt_collection/'
        },
        {
            'name': 'Super Przelew',
            'address': 'super_transfer/'
        },
        {
            'name': 'Usuń pieniądz',
            'address': 'withdraw/'
        },
        {
            'name': 'Dodaj pieniądz',
            'address': 'deposit/'
        },
    ]

    data = {
        'acc': acc,
        'name': f'{req.user.first_name} {req.user.last_name} - {acc.name}',
        'history': history,
        'opcje': opcje,
        'super_opcje': super_opcje,
    }
    return render(req, 'detailed.html', data)


def accept_account_view(req):

    id = req.GET.get('id')
    action = req.GET.get('action')

    if id is not None and action is not None:
        target = get_object_or_404(Account,id=id)
        if not target.active:
            if action == 'yes':
                target.active = True;
                target.save()
            elif action == 'no':
                target.delete()


    rachunki = Account.objects.filter(active = False)

    if not req.user.is_superuser:
        return redirect('/')

    pary = []
    for r in rachunki:
        owner = User.objects.get(username=r.owner)
        pary.append(
            {
                'name': f'{owner.first_name} {owner.last_name} - {r.name}',
                'id': r.id
            }
        )

    data = {
        'konta': pary
    }

    return render(req, 'accept_account.html', data)


def all_accounts_view(req):

    rachunki = Account.objects.filter(active=True)

    if not req.user.is_superuser:
        return redirect('/')

    pary = []
    for r in rachunki:
        owner = User.objects.get(username=r.owner)
        pary.append(
            {
                'name': f'{owner.first_name} {owner.last_name} - {r.name}',
                'balance': r.balance
            }
        )
    pary = sorted(pary, key=lambda x: x['balance'], reverse=True)[1:]
    data = {
        'konta': pary,
    }

    return render(req, 'all_accounts.html', data)
