import pandas as pd
from gym.models import *
from urllib.request import urlopen
import json



def load_initial_gym_data():
    fitness_list = load_csv_file(filename='./resources/fitness center.csv')
    pk = 1
    for i in fitness_list:
        Images = eval(i['Images'])
        G = Gym(gym_name=i['Name'],gym_address=i['Address']+' '+i['Suburb']+' '+i['State']+' '+str(i['Postcode']),gym_limitation=i['Limitation'],gym_coordinate_lat=i['Latitude'],gym_coordinate_long=i['Longitude'])
        G.save()
        G = Gym.objects.get(pk=pk)
        pk+=1
        for j in Images:
            G.image_set.create(image_name=j)


def download_file(url, filename):
    try:
        content = urlopen(url, timeout=15).read()
        jsonContent = json.loads(content.decode('utf-8'))
        with open('./resources/' + filename, 'w', encoding='utf-8') as f:
            f.write(json.dumps(jsonContent))
    except Exception as err:
        print(err)
        print(url)




def download_sensor_location():
    try:
        download_file(
            "https://data.melbourne.vic.gov.au/resource/h57g-5234.json",
            'pedestrian_sensor_location.json')
    except Exception as err:
        print(err)


def store_sensor_location():
    with open("./resources/pedestrian_sensor_location.json",'r') as f:
        content = json.loads(f.read())
    for i in content:
        sensor = Sensor(pk = i['sensor_id'],sensor_name=i['sensor_name'],sensor_coordinate_lat=i['latitude'],sensor_coordinate_long=i['longitude'])
        sensor.save()
def load_csv_file(filename):
    data = pd.read_csv(filename)
    fitness_list = []
    for i, content in data.iterrows():
        fitness_list.append(content.to_dict())
    return fitness_list

def store_sensor_day_data():
    with open('./resources/pedestrian_sensor_location.json','r') as f:
        content = json.loads(f.read())
    weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']

    for i in content:
        sensor = Sensor.objects.get(pk = i['sensor_id'])
        for j in weekdays:
            sensor.daysensor_set.create(day = j,hours = 24)

def initial():
    load_initial_gym_data()
    download_sensor_location()
    store_sensor_location()
    store_sensor_day_data()

