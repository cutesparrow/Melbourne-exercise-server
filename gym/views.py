from math import radians, cos, sin, asin, sqrt
import json
from gym.models import Gym
# Create your views here.
from django.http import HttpResponse

def gymList(request):
    if request.method == 'GET':
        user_lat = request.GET.get('lat',default=0)
        user_long = request.GET.get('long',default=0)
    allGyms = Gym.objects.all()
    result = responseGymList(allGyms,user_lat,user_long)

    return HttpResponse(json.dumps({'list':result}),content_type='application/json')



def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r

def responseGymList(allGyms,user_lat,user_long):
    gymlist = []
    for i in allGyms:
        gymlist.append(ResponseGym(i,user_lat,user_long).__dict__)
    result = sorted(gymlist, key=lambda x: x['distance'],reverse=False)
    return result

class ResponseGym:
    def __init__(self,Gym,user_lat,user_long):
        self.id = Gym.pk
        self.lat = Gym.gym_coordinate_lat
        self.long = Gym.gym_coordinate_long
        self.name = Gym.gym_name
        self.Images = [i.image_name for i in Gym.image_set.all()]
        self.limitation = Gym.gym_limitation
        self.distance = round(haversine(float(user_long),float(user_lat),self.long,self.lat),2)
        self.star = False
        self.address = Gym.gym_address
