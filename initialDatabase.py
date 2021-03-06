import pandas as pd
from gym.models import *
from urllib.request import urlopen
import json
from  jog.models import *


def load_initial_gym_data():
    fitness_list = load_csv_file(filename='./resources/fitness center.csv')
    pk = 1
    for i in fitness_list:
        Images = eval(i['Images'])
        G = Gym(gym_name=i['Name'],gym_address=i['Address']+' '+i['Suburb']+' '+i['State']+' '+str(i['Postcode']),gym_limitation=i['Limitation'],gym_coordinate_lat=i['Latitude'],gym_coordinate_long=i['Longitude'],gym_class=i['Class'],gym_start=i['Start_time'],gym_close=i['End_time'])
        G.save()
        G = Gym.objects.get(pk=pk)
        pk+=1
        for j in Images:
            G.image_set.create(image_name=j)

def load_exercise_into_database():
    list = ['gym','hiking','jogging','walk_dog']
    for i in list:
        E = Exercise(exercise_name=i)
        E.save()

def load_exerciseClassedTip_into_database():
    exercise_tips_list = load_csv_file(filename="./resources/effective_exercise_tips.csv")
    for i in exercise_tips_list:
        tip = ExerciseClassedTip(content=i['Content'],tipClass=i['Category'])
        tip.save()



def load_safety_tips_into_database():
    safety_tips_list = load_csv_file(filename='./resources/safety_tips.csv')
    for i in safety_tips_list:
        type = i['type']
        exercise = Exercise.objects.get(exercise_name=type)
        exercise.safetips_set.create(content=i['content'])

def load_exercise_tips_into_database():
    exercise_tips_list = load_csv_file(filename='./resources/exercise_tips.csv')
    for i in exercise_tips_list:
        type = i['type']
        exercise = Exercise.objects.get(exercise_name=type)
        exercise.exercisetips_set.create(content=i['content'])

def load_safety_policy_into_database():
    safety_policy_list = load_csv_file(filename='./resources/safety_policy.csv')
    for i in safety_policy_list:
        safety_policy = SafetyPolicy(start_date=i['start_date'],title=i['title'],content=i['content'])
        safety_policy.save()

def load_about_covid_into_database():
    about_covid_list = load_csv_file(filename='./resources/about_covid.csv')
    for i in about_covid_list:
        about_covid = AboutCovid(title=i['title'],content=i['content'],background=i['background'],color=i['color'])
        about_covid.save()

def load_exercise_benefits_into_database():
    exercise_benefits = load_csv_file(filename='./resources/exercise_benefit.csv')
    for i in exercise_benefits:
        exercise_benefit = ExerciseBenefits(content=i['content'])
        exercise_benefit.save()

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
    list = []
    for i, content in data.iterrows():
        list.append(content.to_dict())
    return list

def store_sensor_day_data():
    with open('./resources/pedestrian_sensor_location.json','r') as f:
        content = json.loads(f.read())
    weekdays = ['monday','tuesday','wednesday','thursday','friday','saturday','sunday']
    for i in content:
        sensor = Sensor.objects.get(pk = i['sensor_id'])
        for j in weekdays:
            sensor.daysensor_set.create(day = j,hours = 24)



def load_popular_jogging_path_into_database():
    popular_jogging_path_list = load_csv_file(filename='./resources/popular routes.csv')
    for i in popular_jogging_path_list:
        path = PopularJoggingPath(name=i['name']
                                  ,map=i['map']
                                  ,distance=i['distance']
                                  ,elevation=i['elevation']
                                  ,background=i['background']
                                  ,intruduction=i['intruduction']
                                  ,suburb=i['suburb']
                                  ,postcode=i['postcode']
                                  ,latitude=i['latitude']
                                  ,longitude=i['longitude']
                                  ,detail_text=i['detail_text']
                                  ,safety_tips=i['safety_tips'],images=i['images'])
        path.save()

def initial():
    load_initial_gym_data()
    download_sensor_location()
    store_sensor_location()
    store_sensor_day_data()
    load_exercise_into_database()
    load_exercise_tips_into_database()
    load_about_covid_into_database()
    load_safety_policy_into_database()
    load_safety_tips_into_database()
    load_exercise_benefits_into_database()
    load_popular_jogging_path_into_database()
    load_exerciseClassedTip_into_database()

