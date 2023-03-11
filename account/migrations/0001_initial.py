# Generated by Django 4.1.7 on 2023-03-11 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('owner', models.CharField(max_length=127)),
                ('name', models.CharField(max_length=127)),
                ('balance', models.IntegerField(default=0)),
                ('active', models.BooleanField(default=False)),
                ('super', models.BooleanField(default=False)),
            ],
        ),
    ]
