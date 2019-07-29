from django.contrib import admin
from .models import INR_USD_ExchangeRate, Forecasted_INR_USD_ExchangeRate
# Register your models here.

models = ( INR_USD_ExchangeRate, Forecasted_INR_USD_ExchangeRate)
admin.site.register(models)