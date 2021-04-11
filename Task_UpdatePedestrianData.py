from gym.models import *
import pandas as pd
from sodapy import Socrata
import datetime
from jog.models import LastHourSensor

def getDataframe(target):
    client = Socrata("data.melbourne.vic.gov.au", None)
    # Example authenticated client (needed for non-public datasets):
    client = Socrata("data.melbourne.vic.gov.au",
                     "y3laY1SQEM8KJXqu2d6twLnIC",
                      username="shigaoyu615@gmail.com",
                      password="QWEqwe123123..")
    if target == 'monthly':
        results = client.get("b2ak-trbp", limit=50400, order='date_time DESC')
    # 75 sensors, 24 hours per day, 7 days one week, we need at least 2 weeks
    # to predict the data in this week, we need at least 25200 rows data

    # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
    elif target == '15mins':
        results = client.get("d6mv-s43h",limit=5000)
        results_df = pd.DataFrame.from_records(results)
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    else:
        raise InterruptedError
    return results_df

def parserPedestriandata(results_df):
    results_df['hourly_counts'] = pd.to_numeric(results_df['hourly_counts'])
    average = results_df.groupby(['day', 'time', 'sensor_id'])['hourly_counts'].mean()
    maximum = results_df.groupby(['day', 'time', 'sensor_id'])['hourly_counts'].max()
    minimum = results_df.groupby(['day', 'time', 'sensor_id'])['hourly_counts'].min()
    result = pd.concat([average, maximum, minimum], axis=1)
    result.columns = ['average', 'maximum', 'minimum']
    return result

def parserHourlyPedestriandata(result_df):
    result_df['total_of_directions'] = pd.to_numeric(result_df['total_of_directions'])
    result = result_df.groupby(['sensor_id'])['total_of_directions'].mean()
    result = pd.concat([result],axis=1)
    return result

def insertIntodatabase(dataframe):
    HourlyRoadSituation.objects.all().delete()
    print('successfully clean history records')
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))
    for index, content in dataframe.iterrows():
        daySensor = DaySensor.objects.get(day=index[0].lower(),sensor_id=index[-1])
        daySensor.hourlyroadsituation_set.create(hour=index[1],high=content['maximum'],low=content['minimum'],average=content['average'])
    print('successfully insert all new records')
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))


def insertTimelyDataintoDatabase(dataframe):
    LastHourSensor.objects.all().delete()
    print("successfully clean history Last hour sensor data")
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))
    for index, content in dataframe.iterrows():
        sensor = Sensor.objects.get(pk=index)
        sensor.lasthoursensor_set.create(situation=content['total_of_directions'])
    print('successfully insert all new timely sensor records')
    print(datetime.datetime.today().strftime("%Y-%m-%d %H:%M"))


def regularyTaskMonthly():
    dataframe = getDataframe(target='monthly')
    dataframe = parserPedestriandata(dataframe)
    insertIntodatabase(dataframe)

def regularyTaskEvery15Mins():
    dataframe = getDataframe(target='15mins')
    dataframe = parserHourlyPedestriandata(dataframe)
    insertTimelyDataintoDatabase(dataframe)


