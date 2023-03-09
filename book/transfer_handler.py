from account.models import Account
from book.models import Book
from datetime import datetime


def universal_handler(sender_id, receiver_id, value, title, type) -> str:

    try:
        sender = Account.objects.get(id=sender_id)
    except Account.DoesNotExist:
        return 'Konto nie istnieje'

    try:
        receiver = Account.objects.get(id=receiver_id)
    except Account.DoesNotExist:
        return 'Docelowe konto nie istnieje'

    if sender_id == receiver_id:
        return 'Nie można przelać na to konto'


    if sender.balance < value:
        return 'Brak wystarczających środków na koncie'
    if not sender.active:
        return 'Twoje konto jest nieaktywne'
    if not receiver.active:
        return 'Docelowe konto jest nieaktywne'
    if sender.id == receiver.id:
        return 'Nie mozesz przelac do siebie'
    if not value > 0:
        return 'Niezła próba cwaniaczku. Kwota przelewu musi byc wieksza od zera'

    sender.balance -= value
    receiver.balance += value
    sender.save()
    receiver.save()

    book = Book.objects.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        type=type,
        title=title,
        value=value,
        date=datetime.now()
    )

    return ''
