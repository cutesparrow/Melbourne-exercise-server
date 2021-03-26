import pandas as pd
from gym.models import Gym


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

def load_csv_file(filename):
    data = pd.read_csv(filename)
    fitness_list = []
    for i, content in data.iterrows():
        fitness_list.append(content.to_dict())
    return fitness_list

if __name__ == '__main__':
    load_initial_gym_data()