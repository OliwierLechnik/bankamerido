from django.db import models


class Book(models.Model):
    sender_id = models.IntegerField()
    receiver_id = models.IntegerField( )
    type = models.CharField(max_length=127,)
    title = models.CharField(max_length=127)
    value = models.IntegerField()
    date = models.DateField(null=True, blank=True)

