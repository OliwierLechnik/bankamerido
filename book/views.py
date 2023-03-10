from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import RegularTransferForm, DebtCollectionForm, MoneyDepositForm, MoneyWithdrawForm, SuperTransferForm
from account.models import Account
from .transfer_handler import universal_handler
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH


def get_choises(name:str) -> list[tuple[str,str]]:
    accs = Account.objects.filter(active=True)
    users = User.objects.all()

    sets = []
    for acc in accs:
        own = acc.owner
        if own == 'admin':
            continue
        user = users.get(username=own)
        sets.append((acc.id, f'{user.first_name} {user.last_name} - {acc.name}'))

    return [('', f'{name}:')]+sets

# Create your views here.
def regular_transfer_view(req, acc_id):
    if not req.user.is_authenticated:
        return redirect('/')
    acc = get_object_or_404(Account, id=acc_id)
    if not acc.owner == req.user.username:
        return redirect('/')
    if not acc.active:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')

    form = RegularTransferForm(req.POST or None)
    form.fields['acc'] = forms.ChoiceField(choices=get_choises('Konto docelowe'))
    data = {
        'form': form,
        'name': f'{req.user.first_name} {req.user.last_name} - {acc.name}',
        'akcja': 'Przelew'
    }

    if form.is_valid():
        clean = form.cleaned_data

        error = universal_handler(acc_id, clean.get('acc'), clean.get('value'), clean.get('title'), 'regular_transfer')
        if error == '':
            return redirect(f'../')
        else:
            data['error'] = error
            print(error)
    return render(req, 'transfer.html', data)


def whole_history_view(req, acc_id):
    acc = get_object_or_404(Account, id=acc_id)

    if not req.user.is_authenticated:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')
    if not acc.super:
        return redirect('../')

    slownik = {
        'regular_transfer': 'Przelew',
        'super_transfer': 'Zaj??cie komornicze',
        'deposit': 'Wp??ata',
        'withdraw': 'Wyp??ata',
        'debt_collection': 'Windykacja',
    }

    global_history = []
    for book in Book.objects.all():
        sender = Account.objects.get(id=book.sender_id)
        receiver = Account.objects.get(id=book.receiver_id)
        sender_owner = User.objects.get(username=sender.owner)
        receiver_owner = User.objects.get(username=receiver.owner)
        global_history.append(
            {
                'title': book.title,
                'date': datetime.strftime(book.date, '%d-%m-%Y'),
                'sender': f'{sender_owner.first_name} {sender_owner.last_name} - {sender.name}',
                'receiver': f'{receiver_owner.first_name} {receiver_owner.last_name} - {receiver.name}',
                'value': book.value,
                'id': book.id,
                'type': slownik.get(book.type)
            }
        )

    data = {
        'history': sorted(global_history, key=lambda x: x.get('id'), reverse=True),
    }

    return render(req, 'history.html', data)


def debt_collection_view(req, acc_id):
    acc = get_object_or_404(Account, id=acc_id)

    if not req.user.is_authenticated:
        return redirect('/')
    if not acc.super:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')

    form = DebtCollectionForm(req.POST or None)
    form.fields['acc'] = forms.ChoiceField(choices=get_choises('Konto Docelowe'))
    data = {
        'form': form,
        'akcja': 'Windykacja'
    }
    if form.is_valid():
        clean = form.cleaned_data

        debtor_id = clean.get('acc')
        value = clean.get('value')
        title = clean.get('title')

        error = universal_handler(debtor_id, acc_id, value, title, 'debt_collection')

        if error == '':
            return redirect('../')
        else:
            data['error'] = error

    return render(req, 'transfer.html', data)


def money_withdraw_view(req, acc_id):
    acc = get_object_or_404(Account, id=acc_id)

    if not req.user.is_authenticated:
        return redirect('/')
    if not acc.super:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')

    form = MoneyWithdrawForm(req.POST or None)
    form.fields['acc'] = forms.ChoiceField(choices=get_choises('Konto Docelowe'))
    data = {
        'form': form,
        'akcja': 'Wyp??ata ??rodk??w'
    }
    if form.is_valid():
        clean = form.cleaned_data

        target = clean.get('acc')
        value = clean.get('value')

        host = Account.objects.get(owner='admin')

        error = universal_handler(target, host.id, value, 'Wyp??ata ??rodk??w z konta', 'withdraw')

        if error == '':
            return redirect('../')
        else:
            data['error'] = error

    return render(req, 'transfer.html', data)


def money_deposit_view(req, acc_id):

    acc = Account.objects.get(id=acc_id)
    if not req.user.is_authenticated:
        return redirect('/')
    if not acc.super:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')


    form = MoneyDepositForm(req.POST or None)
    form.fields['acc'] = forms.ChoiceField(choices=get_choises('Konto Docelowe'))
    data = {
        'form': form,
        'akcja': 'Wp??ata ??rodk??w'
    }
    if form.is_valid():
        clean = form.cleaned_data

        target = clean.get('acc')
        value = clean.get('value')

        host = Account.objects.get(owner='admin')

        error = universal_handler(host.id, target, value, 'Wp??ata ??rodk??w na konto', 'deposit')

        if error == '':
            return redirect('../')
        else:
            data['error'] = error

    return render(req, 'transfer.html', data)


def super_transfer_view(req, acc_id):
    if not req.user.is_authenticated:
        return redirect('/')
    acc = get_object_or_404(Account, id=acc_id)
    if not acc.owner == req.user.username:
        return redirect('/')
    if not acc.active:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')

    form = SuperTransferForm(req.POST or None)
    form.fields['source'] = forms.ChoiceField(choices=get_choises('Wybierz ??r??d??o'))
    form.fields['destination'] = forms.ChoiceField(choices=get_choises('Wybierz odbiorce'))
    data = {
        'form': form,
        'name': f'{req.user.first_name} {req.user.last_name} - {acc.name}',
        'akcja': 'Super przelew'
    }

    if form.is_valid():
        clean = form.cleaned_data

        error = universal_handler(clean.get('source'), clean.get('destination'), clean.get('value'), clean.get('title'),
                                  'super_transfer')
        if error == '':
            return redirect(f'../')
        else:
            data['error'] = error
            print(error)
    return render(req, 'transfer.html', data)
