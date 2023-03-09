from account.models import Account
from book.models import Book
from datetime import datetime


def regular_transter(order, sender_id, receiver_id, value, title) -> str:
    try:
        sender = Account.objects.get(id=sender_id)
    except Account.DoesNotExist:
        return 'Twoje konto nie istnieje'

    try:
        receiver = Account.objects.get(id=receiver_id)
    except Account.DoesNotExist:
        return 'Docelowe konto nie istnieje'

    if not sender.balance >= value:
        return 'Brak wystarczających środkow na koncie'
    if not order.username == sender.owner:
        return 'Niezgodny autor przelewu'
    if not sender.active:
        return 'Twoje konto jest nieaktywne'
    if not receiver.active:
        return 'Docelowe konto jest nieaktywne'
    if sender.id == receiver.id:
        return 'Nie mozesz przelac do siebie'
    if not order.username == sender.owner:
        return 'Nie jestes wlascicielem tego konta'
    if not value > 0:
        return 'Niezła próba cwaniaczku. Kwota przelewu musi byc wieksza od zera'

    sender.balance -= value
    receiver.balance += value
    sender.save()
    receiver.save()

    book = Book.objects.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        type='regular_transfer',
        title=title,
        value=value,
        date=datetime.now()
    )

    return ''
