from django.db import models


class Book(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField( )
    type = models.CharField(max_length=127,)
    title = models.CharField(max_length=127)
    value = models.DecimalField(max_digits=100, decimal_places=2)
    date = models.DateField(null=True, blank=True)

