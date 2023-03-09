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
        if own == 'admin':
            continue
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

    def __int__(self, *args, **kwargs):
        super(RegularTransferForm, self).__init__(*args, **kwargs)
        self.fields['acc'] = forms.ChoiceField(choices=get_choises())

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

    def __int__(self, *args, **kwargs):
        super(SuperTransferForm, self).__init__(*args, **kwargs)
        self.fields['source'] = forms.ChoiceField(choices=get_choises())
        self.fields['destination'] = forms.ChoiceField(choices=get_choises())

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
    def __int__(self, *args, **kwargs):
        super(DebtCollectionForm, self).__init__(*args, **kwargs)
        self.fields['acc'] = forms.ChoiceField(choices=get_choises())
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
    def __int__(self, choises, *args, **kwargs):
        super(MoneyWithdrawForm, self).__init__(*args, **kwargs)
        self.fields['acc'].choises = choises
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

    def __int__(self, *args, **kwargs):
        super(MoneyDepositForm, self).__init__(*args, **kwargs)
        self.fields['acc'] = forms.ChoiceField(choices=get_choises())
