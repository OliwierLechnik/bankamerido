from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'owner', 'name', 'balance','credit', 'active', 'super')

# Register your models here.
