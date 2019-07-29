# Generated by Django 2.2.3 on 2019-07-28 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exchange_rate', '0002_auto_20190728_1808'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='inr_usd_exchangerate',
            options={'verbose_name': 'INR_USD_RATE', 'verbose_name_plural': 'INR_USD_RATES'},
        ),
        migrations.AlterField(
            model_name='inr_usd_exchangerate',
            name='date',
            field=models.DateField(unique=True),
        ),
    ]
