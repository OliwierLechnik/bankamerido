from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import RegularTransferForm
from account.models import Account
from .transfer_handler import regular_transter
from django.contrib.auth.models import User
from datetime import datetime

# Create your views here.
def regular_transfer_view(req, acc_id):
    if not req.user.is_authenticated:
        return redirect('/')
    acc = get_object_or_404(Account, id=acc_id)
    if not acc.owner == req.user.username:
        return redirect('/')
    if not acc.active:
        return redirect('/')

    form = RegularTransferForm(req.POST or None)
    data = {
        'form': form,
        'name': f'{req.user.first_name} {req.user.last_name} - {acc.name}'
    }

    if form.is_valid():
        clean = form.cleaned_data
        error = regular_transter(req.user, acc_id, clean.get('acc'), clean.get('value'), clean.get('title'))
        print(error)
        if error == '':
            return redirect(f'../')
        else:
            data['error'] = error
            print(error)
    return render(req, 'transfer.html', data)


def whole_history_view(req, acc_id):
    acc = get_object_or_404(Account, id=acc_id)
    if not req.user.username == acc.owner:
        return redirect('/')
    if not acc.super:
        return redirect('../')

    global_history = []
    for book in Book.objects.all():
        sender = Account.objects.get(id = book.sender_id)
        receiver = Account.objects.get(id = book.receiver_id)
        sender_owner = User.objects.get(username = sender.owner)
        receiver_owner = User.objects.get(username = receiver.owner)
        global_history.append(
            {
                'title': book.title,
                'date': datetime.strftime(book.date, '%d-%m-%Y'),
                'sender': f'{sender_owner.first_name} {sender_owner.last_name} - {sender.name}',
                'receiver': f'{receiver_owner.first_name} {receiver_owner.last_name} - {receiver.name}',
                'value': book.value,
                'id': book.id,
            }
        )

    data = {
        'history': sorted(global_history, key=lambda x:x.get('id'), reverse=True),
    }

    return render(req, 'history.html', data)
