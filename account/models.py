from django.db import models


class Account(models.Model):
    owner = models.CharField(max_length=127)
    name = models.CharField(max_length=127)
    balance = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=100, decimal_places=2, default=0)
    active = models.BooleanField(default=False)
    super = models.BooleanField(default=False)
    block_incoming = models.BooleanField(default=False)
    block_outgoing = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} - {self.name} (ID: {self.id})'

