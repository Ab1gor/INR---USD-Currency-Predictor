from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import datetime, numpy, pandas, threading
from pandas import Series
import numpy as np
import pandas as pd, pickle
from chartit import DataPool, Chart
from .models import INR_USD_ExchangeRate, Forecasted_INR_USD_ExchangeRate
from urban_assignment.settings import model_name
from .utils import forecast_new_dates, real_data_fetcher

# Create your views here.

def current_datetime(request):
    try:
        data = request.POST.copy()

        if data['start_date'] > data['max_date']:
            return render(request, "dashboard.html")

        threading.Thread(target=real_data_fetcher, args=(data,)).start()

        start_date = datetime.datetime.strptime( data['start_date'] , "%Y-%m-%d")
        end_date = datetime.datetime.strptime( data['max_date'] , "%Y-%m-%d")
        delta = end_date - start_date

        #Step 1: Create a DataPool with the data we want to retrieve.

        forecasted_queryset = Forecasted_INR_USD_ExchangeRate.objects.filter(date__gte=data['start_date'], date__lte=data['max_date'])

        if len(forecasted_queryset) < delta.days:

            forecast_new_dates(data)
            forecasted_queryset = Forecasted_INR_USD_ExchangeRate.objects.filter(date__gte=data['start_date'], date__lte=data['max_date'])


        inr_usd_data = \
            DataPool(
               series=
                [{'options': {
                   'source': forecasted_queryset},
                  'terms': [
                    'date',
                    'inr_rate']}
                 ])

        #Step 2: Create the Chart object
        cht = Chart(
                datasource = inr_usd_data,
                series_options =
                  [{'options':{
                      'type': 'line',
                      'stacking': False},
                    'terms':{
                      'date': [
                        'inr_rate']
                      }}],
                chart_options =
                  {'title': {
                       'text': 'INR value with respect to 1 USD'},
                   'xAxis': {
                        'title': {
                           'text': 'Month number'}}})
    	
        #Step 3: Send the chart object to the template.
        return render(request, "rate_chart.html", context = {'inr_usd_data': cht})
    except:
        return render(request, "dashboard.html")

def dashboard(request):

  return render(request, "dashboard.html")