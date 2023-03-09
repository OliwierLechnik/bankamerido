from django import forms
from .models import Book
from django.db.models.fields import BLANK_CHOICE_DASH
from account.models import Account
from django.contrib.auth.models import User

def get_choises() -> list[tuple[str,str]]:
    accs = Account.objects.filter(active=True)
    users = User.objects.all()

    sets = []
    for acc in accs:
        own = acc.owner
        user = users.get(username=own)
        sets.append((acc.id, f'{user.first_name} {user.last_name} - {acc.name}'))

    return sets


class RegularTransferForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz odbiorce:')] + get_choises(),
        required=True
        )
    title = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tytuł',
            },
        )
    )
    value = forms.IntegerField(
        label='',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Kwota',
            },
        )
    )
    fields = [
        'acc',
        'title',
        'value'
    ]

class SuperTransferForm(forms.Form):
    source = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz źródło:')] + get_choises(),
        required=True
        )
    destination = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz cel:')] + get_choises(),
        required=True
        )
    title = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tytuł',
            },
        )
    )
    value = forms.IntegerField(
        label='',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Kwota',
            },
        )
    )
    fields = [
        'source',
        'destination',
        'title',
        'value'
    ]

class DebtCollectionForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz Dłużnika:')] + get_choises(),
        required=True
        )
    title = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Tytuł',
            },
        )
    )
    value = forms.IntegerField(
        label='',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Kwota',
            },
        )
    )
    fields = [
        'acc',
        'title',
        'value'
    ]

class MoneyWithdrawForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Docelowe konto:')] + get_choises(),
        required=True
        )
    value = forms.IntegerField(
        label='',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Kwota',
            },
        )
    )
    fields = [
        'acc',
        'value'
    ]
class MoneyDepositForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Docelowe konto:')] + get_choises(),
        required=True
        )
    value = forms.IntegerField(
        label='',
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': 'Kwota',
            },
        )
    )
    fields = [
        'acc',
        'value'
    ]

