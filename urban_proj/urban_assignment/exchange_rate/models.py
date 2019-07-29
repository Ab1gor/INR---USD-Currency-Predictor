from django.db import models

# Create your models here.

class INR_USD_ExchangeRate(models.Model):

    inr_rate = models.FloatField(
        blank=False,
        null=False)

    usd_rate = models.FloatField(
        blank=False,
        null=False)

    date = models.DateField(
        unique=True,
    	blank=False,
        null=False)

    class Meta:
        verbose_name = "INR_USD_RATE"
        verbose_name_plural = "INR_USD_RATES"

    def __str__(self):
        return str(self.date)


class Forecasted_INR_USD_ExchangeRate(models.Model):

    inr_rate = models.FloatField(
        blank=False,
        null=False)

    usd_rate = models.FloatField(
        blank=False,
        null=False)

    date = models.DateField(
        unique=True,
        blank=False,
        null=False)

    class Meta:
        verbose_name = "Forecasted INR_USD_RATE"
        verbose_name_plural = "Forecasted INR_USD_RATES"

    def __str__(self):
        return str(self.date)