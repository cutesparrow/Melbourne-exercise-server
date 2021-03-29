from gym.models import *
import pandas as pd
from sodapy import Socrata


def getDataframe():
    client = Socrata("data.melbourne.vic.gov.au", None)
    # Example authenticated client (needed for non-public datasets):
    client = Socrata("data.melbourne.vic.gov.au",
                     "y3laY1SQEM8KJXqu2d6twLnIC",
                      username="shigaoyu615@gmail.com",
                      password="QWEqwe123123..")

    results = client.get("b2ak-trbp", limit=50400, order='date_time DESC')
    # 75 sensors, 24 hours per day, 7 days one week, we need at least 2 weeks
    # to predict the data in this week, we need at least 25200 rows data

    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    # Unauthenticated client only works with public data sets. Note 'None'
    # in place of application token, and no username or password:
    return results_df

def parserPedestriandata(results_df):
    results_df['hourly_counts'] = pd.to_numeric(results_df['hourly_counts'])
    average = results_df.groupby(['day', 'time', 'sensor_id'])['hourly_counts'].mean()
    maximum = results_df.groupby(['day', 'time', 'sensor_id'])['hourly_counts'].max()
    minimum = results_df.groupby(['day', 'time', 'sensor_id'])['hourly_counts'].min()
    result = pd.concat([average, maximum, minimum], axis=1)
    result.columns = ['average', 'maximum', 'minimum']
    return result


def insertIntodatabase(dataframe):
    for index, content in dataframe.iterrows():
        daySensor = DaySensor.objects.get(day=index[0].lower(),sensor_id=index[-1])
        daySensor.hourlyroadsituation_set.create(hour=index[1],high=content['maximum'],low=content['minimum'],average=content['average'])


def regularyTask():
    dataframe = getDataframe()
    dataframe = parserPedestriandata(dataframe)
    insertIntodatabase(dataframe)

