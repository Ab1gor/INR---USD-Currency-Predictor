# Generated by Django 2.2.3 on 2019-07-28 18:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_rate', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ChildAssessment',
            new_name='INR_USD_ExchangeRate',
        ),
    ]
