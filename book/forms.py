from django import forms

class RegularTransferForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz odbiorce:')],
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

class SuperTransferForm(forms.Form):
    source = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz źródło:')],
        required=True
        )
    destination = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz cel:')],
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

class DebtCollectionForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Wybierz Dłużnika:')],
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

class DebtCollectionGroupForm(forms.Form):
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
    zacc = None
    # fields = ['title','value','acc']

class MoneyWithdrawForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Docelowe konto:')],
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
class MoneyDepositForm(forms.Form):
    acc = forms.ChoiceField(
        label='Konto docelowe',
        choices=[('', 'Docelowe konto:')],
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