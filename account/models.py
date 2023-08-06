from django.db import models


class Account(models.Model):
    owner = models.CharField(max_length=127)
    name = models.CharField(max_length=127)
    balance = models.IntegerField(default=0)
    credit = models.IntegerField(default=0)
    active = models.BooleanField(default=False)
    super = models.BooleanField(default=False)

