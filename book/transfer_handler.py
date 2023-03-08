from account.models import Account
from book.models import Book
from datetime import datetime


def regular_transter(sender_id, receiver_id, value, title):
    sender = Account.objects.get(id=sender_id)
    receiver = Account.objects.get(id=receiver_id)

    if not sender.balance >= value:
        return False

    sender.balance -= value
    receiver.balance += value

    book = Book.object.create(
        sender_id=sender_id,
        receiver_id=receiver_id,
        type='regular_transfer',
        title=title,
        value=value,
        date=datetime.now()
    )

    return True
