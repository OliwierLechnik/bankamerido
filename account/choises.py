from .models import Account
from django.contrib.auth.models import User


def get_choises() -> list[tuple[str,str]]:
    accs = Account.objects.filter(active=True)
    users = User.objects.all()

    sets = []
    for acc in accs:
        own = acc.owner
        user = users.get(username=own)
        sets.append((acc.id, f'{user.first_name} {user.last_name} {acc.name}'))

    return sets



