import time, requests, datetime, threading
from dateutil.relativedelta import relativedelta
from urban_assignment.settings import model_name

from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
import numpy as np
import pandas as pd, pickle
from sklearn import linear_model

from exchange_rate.models import INR_USD_ExchangeRate

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")


def train_model():
    try:
        # api-endpoint
        training_date_list = INR_USD_ExchangeRate.objects.all().order_by('date').values_list('date', flat=True)
        training_inr_rate_list = INR_USD_ExchangeRate.objects.all().order_by('date').values_list('inr_rate', flat=True)
        
        data_date = np.asarray( training_date_list )
        data_inr = np.asarray( training_inr_rate_list )

        # df = pd.DataFrame({'time': data_date, 'inr': data_inr}, index = 0)
        df_inr = pd.DataFrame( training_inr_rate_list )
        df_date = pd.to_datetime( training_date_list )

        model = linear_model.LinearRegression()
        model.fit(df_date.values.reshape(-1, 1), df_inr.values.reshape(-1, 1))
        model.predict(df_date.values.astype(float).reshape(-1, 1))

        pickle.dump(model, open(model_name, 'wb'))

        print("Training data complete")

    except Exception as error:
        print(str(error))

@register_job(scheduler, "cron", hour='0')
def test_job():
    try:
        # api-endpoint 
        URL = "https://api.exchangeratesapi.io/history"
          
        # defining a params dict for the parameters to be sent to the API 
        PARAMS = {
                    'start_at': datetime.date.today() - relativedelta(months=2),
                    'end_at' : datetime.date.today(),
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

    except Exception as error:
        print(str(error))

register_events(scheduler)

scheduler.start()
print("Scheduler started!")