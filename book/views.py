from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from .forms import RegularTransferForm
from account.models import Account
from account.choises import get_choises

# Create your views here.
def regular_transfer_view(req, acc_id):
    if not req.user.is_authenticated:
        return redirect('/')
    acc = get_object_or_404(Account, id=acc_id)
    if not acc.owner == req.user.username:
        return redirect('/')
    if not acc.active:
        return redirect('/')
    print(get_choises())

    form = RegularTransferForm(req.POST or None)
    data = {
        'form': form,
    }

    if form.is_valid():
        pass

    return render(req, 'transfer.html', data)
    