from django.db import models


# Create your models here.
class Book(models.Model):
    sender_id: models.IntegerField()
    receiver_id: models.IntegerField()
    type: models.Choices(['A', 'B', 'C'])
    title: models.CharField(max_length=127)
    value: models.IntegerField()

