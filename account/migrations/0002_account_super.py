# Generated by Django 4.1.7 on 2023-03-06 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='super',
            field=models.BooleanField(default=False),
        ),
    ]