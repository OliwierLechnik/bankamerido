from account.models import Account
from book.models import Book
from datetime import datetime
from django.contrib.auth.models import User


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

def group_handler(senders_id: list, receivers_id: list, value, title, type) -> str:
    def validate(iteratable, func, *args) -> list:
        """
            @brief: validate which values satisfie condition
            @param iteratable: iteratable
            @param func: function that returns boolean.
            @param *args: other arguments for a function func()
            @return: all values that do not evaluate to False
        """
        out = []
        for i in iteratable:
            if not func(i, *args):
                out.append(i)
        return out
    
    senders = set()
    for sender_id in senders_id:
        try:
            senders.add(Account.objects.get(id=sender_id))
        except Account.DoesNotExist:
            return f'Konto nie o id {sender_id} istnieje.'
    receivers = set()
    for receiver_id in receivers_id:
        try:
            receivers.add(Account.objects.get(id=receiver_id))
        except Account.DoesNotExist:
            return f'Docelowe konto o id {receiver_id} nie istnieje.'

    if not ((len(senders) == 1) or (len(receivers) == 1)):
        return f'Nie można przelać srodków. \
            Nie poprawna ilość kont po obu stronach \
                ({len(senders)} wysyłających i {len(receivers)} odbierających).'

    outgoing = len(receivers) * value
    incomming = len(senders) * value

    # print(senders)
    poor = validate(senders, lambda i,v: i.balance >= v, outgoing)
    inactive_senders = validate(senders, lambda i: i.active)
    inactive_receivers = validate(receivers, lambda i: i.active)

    if len(poor) > 0:
        return f'Konta z niewystarczającą ilością środków: {",".join([f"{User.objects.get(username=p.owner).first_name} {User.objects.get(username=p.owner).last_name} - {p.name}"for p in poor])}.'
    if len(inactive_senders):
        return f'Błąd konta: {",".join([f"{User.objects.get(username=p.owner).first_name} {User.objects.get(username=p.owner).last_name} - {p.name}" for p in inactive_senders])} są nieaktywne.'
    if len(inactive_receivers):
        return f'Błąd konta: {",".join([f"{User.objects.get(username=p.owner).first_name} {User.objects.get(username=p.owner).last_name} - {p.name}" for p in inactive_receivers])} są nieaktywne.'
    
    if (list(receivers)[0] in senders) or (list(senders)[0] in receivers):
        return 'Nie mozesz przelac do siebie.'
    
    if not value > 0:
        return 'Niezła próba cwaniaczku. Kwota przelewu musi byc wieksza od zera'


    for sender in senders:
        sender.balance -= outgoing
        sender.save()
    for receiver in receivers:
        receiver.balance += incomming
        receiver.save()

    for sender in senders:
        for receiver in receivers:
            book = Book.objects.create(
                sender_id=sender.id,
                receiver_id=receiver.id,
                type=type,
                title=title,
                value=value,
                date=datetime.now()
            )

    return ''
