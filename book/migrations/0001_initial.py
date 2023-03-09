# Generated by Django 4.1.7 on 2023-03-09 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sender_id', models.IntegerField()),
                ('receiver_id', models.IntegerField()),
                ('type', models.CharField(max_length=127)),
                ('title', models.CharField(max_length=127)),
                ('value', models.IntegerField()),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
    ]