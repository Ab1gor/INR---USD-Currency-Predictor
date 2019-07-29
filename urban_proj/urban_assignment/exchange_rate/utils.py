from .models import INR_USD_ExchangeRate, Forecasted_INR_USD_ExchangeRate
import datetime, numpy, pandas, requests
from pandas import Series
import numpy as np
import pandas as pd, pickle
from urban_assignment.settings import model_name
from urban_assignment.jobs import train_model
from dateutil.relativedelta import relativedelta



def forecast_new_dates(data):
    start_date = datetime.datetime.strptime( data['start_date'] , "%Y-%m-%d")
    end_date = datetime.datetime.strptime( data['max_date'] , "%Y-%m-%d")

    delta = end_date - start_date
    loaded_model = pickle.load(open(model_name, 'rb'))

    for i in range(delta.days + 1):
        day = start_date + datetime.timedelta(days=i)
        forecasted_obj_temp = Forecasted_INR_USD_ExchangeRate.objects.filter(date=day).first()

        if not forecasted_obj_temp:
            forecasted_obj_temp = Forecasted_INR_USD_ExchangeRate()

        forecasted_obj_temp.usd_rate = 1.0
        forecasted_obj_temp.date = day
        df_date = pd.to_datetime( [ str(day.date()) ] )

        forecasted_obj_temp.inr_rate = loaded_model.predict(df_date.values.astype(float).reshape(-1, 1))

        forecasted_obj_temp.save()

def real_data_fetcher(data):
    start_date = datetime.datetime.strptime( data['start_date'] , "%Y-%m-%d")
    end_date = datetime.datetime.strptime( data['max_date'] , "%Y-%m-%d")

    real_data = INR_USD_ExchangeRate.objects.filter(date = start_date - relativedelta(months=2) ).first()

    if not real_data:

        URL = "https://api.exchangeratesapi.io/history"
          
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {
                    'start_at': (start_date - relativedelta(months=2)).date(),
                    'end_at' : end_date.date(),
                    'symbols' : 'USD,INR',
                    'base' : 'USD'
                } 
          
        # sending get request and saving the response as response object 
        r = requests.get(url = URL, params = PARAMS) 
          
        # extracting data in json format 
        data_dict = r.json()
        date_keys = data_dict['rates'].keys()

        for date in date_keys:
            try:
                inr_usd_exchangerate_api = INR_USD_ExchangeRate()
                inr_usd_exchangerate_api.inr_rate = data_dict['rates'][date]['INR']
                inr_usd_exchangerate_api.usd_rate = data_dict['rates'][date]['USD']
                inr_usd_exchangerate_api.date = date
                inr_usd_exchangerate_api.save()
            except:
                pass

        train_model()

