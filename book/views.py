from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import RegularTransferForm, DebtCollectionForm, MoneyDepositForm, MoneyWithdrawForm, SuperTransferForm, DebtCollectionGroupForm
from account.models import Account
from .transfer_handler import universal_handler, group_handler
from django.contrib.auth.models import User
from datetime import datetime
from django import forms
from django.db.models.fields import BLANK_CHOICE_DASH


def get_choices(name:str) -> list[tuple[str,str]]:
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
    form.fields['acc'] = forms.ChoiceField(choices=get_choices('Konto docelowe'))
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


def whole_history_view(req, acc_id, page):
    chunk = 25
    acc = get_object_or_404(Account, id=acc_id)

    if not req.user.is_authenticated:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')
    if not acc.super:
        return redirect('../')

    slownik = {
        'regular_transfer': 'Przelew',
        'super_transfer': 'Zajęcie komornicze',
        'deposit': 'Wpłata',
        'withdraw': 'Wypłata',
        'debt_collection': 'Windykacja',
    }

    global_history = []
    for book in Book.objects.all().order_by('-id')[chunk*(page-1):chunk*page]:
        try:
            sender = Account.objects.get(id=book.sender_id)
            sender_owner = User.objects.get(username=sender.owner)
            sender_txt = f'{sender_owner.first_name} {sender_owner.last_name} - {sender.name}'
        except:
            sender_txt = f'Konto usunięte id={book.sender_id}'

        try:
            receiver = Account.objects.get(id=book.receiver_id)
            receiver_owner = User.objects.get(username=receiver.owner)
            receiver_txt = f'{receiver_owner.first_name} {receiver_owner.last_name} - {receiver.name}'
        except:
            receiver_txt = f'Konto usunięte id={book.sender_id}'

        global_history.append(
            {
                'title': book.title,
                'date': datetime.strftime(book.date, '%d-%m-%Y'),
                'sender': sender_txt,
                'receiver': receiver_txt,
                'value': book.value,
                'id': book.id,
                'type': slownik.get(book.type)
            }
        )

    data = {
        'history': global_history,
        'prev': page-1 if page-1 > 0 else 1,
        'next': page+1
    }

    return render(req, 'history.html', data)


def debt_collection_group_view(req, acc_id):
    acc = get_object_or_404(Account, id=acc_id)

    if not req.user.is_authenticated:
        return redirect('/')
    if not acc.super:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')

    form = DebtCollectionGroupForm(req.POST or None)
    c = get_choices('Konto Docelowe')[1:]
    # for ci in c:
    #     print(ascii(ci))
    form.fields['zacc'] = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple, 
        required=True, 
        choices=c
    )
    data = {
        'form': form,
        'akcja': 'Windykacja'
    }
    if form.is_valid():
        clean = form.cleaned_data

        value = clean.get('value')
        title = clean.get('title')
        debtors_id = clean.get('zacc')
        # print(debtor_id)
        if len(debtors_id) == 0:
            form.errors = []
        else:
            error = group_handler(debtors_id, [acc_id], value, title, 'debt_collection')
        # error = None

        if error == '':
            return redirect('../')
        else:
            data['error'] = error

    return render(req, 'transfer.html', data)


def debt_collection_view(req, acc_id):
    acc = get_object_or_404(Account, id=acc_id)

    if not req.user.is_authenticated:
        return redirect('/')
    if not acc.super:
        return redirect('/')
    if not req.user.username == acc.owner:
        return redirect('/')

    form = DebtCollectionForm(req.POST or None)
    form.fields['acc'] = forms.ChoiceField(choices=get_choices('Konto Docelowe'))
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
    form.fields['acc'] = forms.ChoiceField(choices=get_choices('Konto Docelowe'))
    data = {
        'form': form,
        'akcja': 'Wypłata środków'
    }
    if form.is_valid():
        clean = form.cleaned_data

        target = clean.get('acc')
        value = clean.get('value')

        host = Account.objects.get(owner='admin')

        error = universal_handler(target, host.id, value, 'Wypłata środków z konta', 'withdraw')

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
    form.fields['acc'] = forms.ChoiceField(choices=get_choices('Konto Docelowe'))
    data = {
        'form': form,
        'akcja': 'Wpłata środków'
    }
    if form.is_valid():
        clean = form.cleaned_data

        target = clean.get('acc')
        value = clean.get('value')

        host = Account.objects.get(owner='admin')

        error = universal_handler(host.id, target, value, 'Wpłata środków na konto', 'deposit')

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
    form.fields['source'] = forms.ChoiceField(choices=get_choices('Wybierz źródło'))
    form.fields['destination'] = forms.ChoiceField(choices=get_choices('Wybierz odbiorce'))
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
