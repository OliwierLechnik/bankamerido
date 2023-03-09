from django.forms import ModelForm
from .models import Account

class AccountCreationForm(ModelForm):
    class Meta:
        model = Account
        fields = ['name']

