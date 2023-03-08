from django import forms
from .models import Book
from django.db.models.fields import BLANK_CHOICE_DASH
from account.choises import get_choises


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


