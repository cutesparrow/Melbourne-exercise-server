from math import radians, cos, sin, asin, sqrt
import json
from gym.models import *
# Create your views here.
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseForbidden
from datetime import datetime
from functools import wraps
from django.views.decorators.http import require_GET

def valid_request(f):
    """
    check request header token. Only accept request from app
    :param f:
    :return:
    """
    @wraps(f)
    def decorated_function(request, *args, **kwargs):
        validator = '2c4092daa53543069e0800b12522463c'
        valid_result = request.META.get("HTTP_ACCESS_TOKEN") == validator
        if valid_result:
            return f(request, *args, **kwargs)
        else:
            return HttpResponseForbidden()
    return decorated_function

class RoadSituation:
    def __init__(self,day,situation,hours):
        self.day = day
        self.situation = situation
        self.hours = hours

class OneHourRoadSituation:
    def __init__(self,hour,high,low,average):
        self.hour = hour
        self.high = high
        self.low = low
        self.average = average

@require_GET
@valid_request
def gymList(request):
    if request.method == 'GET':
        user_lat = request.GET.get('lat',default=0)
        user_long = request.GET.get('long',default=0)
    allGyms = Gym.objects.all()
    result = responseGymList(allGyms,user_lat,user_long)
    return HttpResponse(json.dumps({'list':result}),content_type='application/json')



def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])


    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371
    return c * r

def responseGymList(allGyms,user_lat,user_long):
    """
    response gym list and sorted by distance to userlocation
    :param allGyms:
    :param user_lat:
    :param user_long:
    :return:
    """
    gymlist = []
    for i in allGyms:
        gymlist.append(ResponseGym(i,user_lat,user_long).__dict__)
    result = sorted(gymlist, key=lambda x: x['distance'],reverse=False)
    return result

def getWeekDay(num):
    if num == 0:
        return 'monday'
    elif num == 1:
        return 'tuesday'
    elif num == 2:
        return 'wednesday'
    elif num == 3:
        return 'thursday'
    elif num == 4:
        return 'friday'
    elif num == 5:
        return 'saturday'
    elif num == 6:
        return 'sunday'



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
        self.classType = Gym.gym_class

def findAllRelatedSensor(gym_lat,gym_long,user_lat,user_long):

    """
    based on user location and target location
    find out sensor on the path, if no sensor , use the cloest one
    :param gym_lat:
    :param gym_long:
    :param user_lat:
    :param user_long:
    :return:
    """
    today = datetime.now().weekday()
    tomorrow = today + 1
    if tomorrow == 7:
        tomorrow = 0
    today = getWeekDay(today)
    tomorrow = getWeekDay(tomorrow)
    big_lat,small_lat = (gym_lat,user_lat) if gym_lat > user_lat else (user_lat,gym_lat)
    big_long,small_long = (gym_long,user_long) if gym_long>user_long else (user_long,gym_long)
    sensor_list = Sensor.objects.filter(sensor_coordinate_lat__gte = small_lat,
                                        sensor_coordinate_lat__lte = big_lat,
                                        sensor_coordinate_long__gte = small_long,
                                        sensor_coordinate_long__lte = big_long)
    sensor_list = list(sensor_list)
    for i in sensor_list:
        daySensor = DaySensor.objects.get(sensor_id = i.id,day = today)
        daySensor_tomorrow = DaySensor.objects.get(sensor_id = i.id, day = tomorrow)
        check_today = HourlyRoadSituation.objects.filter(day_sensor_id=daySensor.id)
        check_tomorrow = HourlyRoadSituation.objects.filter(day_sensor_id=daySensor_tomorrow.id)
        if check_today.exists() and check_tomorrow.exists():
            continue
        else:
            del sensor_list[sensor_list.index(i)]

    if len(sensor_list) == 0:
        lat = (gym_lat + user_lat)/2
        long = (gym_long + user_long)/2
        distance = 2**31
        close_sensor = None
        for i in Sensor.objects.all():
            daySensor = DaySensor.objects.get(sensor_id=i.id, day=today)
            daySensor_tomorrow = DaySensor.objects.get(sensor_id=i.id, day=tomorrow)
            check_today = HourlyRoadSituation.objects.filter(day_sensor_id=daySensor.id)
            check_tomorrow = HourlyRoadSituation.objects.filter(day_sensor_id=daySensor_tomorrow.id)
            if haversine(lat,long,i.sensor_coordinate_lat,i.sensor_coordinate_long) < distance and check_today.exists() and check_tomorrow.exists():
                close_sensor = i.id
        sensor_list = Sensor.objects.filter(pk=close_sensor)
    return sensor_list

def getSituationList(sensors,weekday,distance):
    """
    the risk number is calculated with sensor data distance and time cost on road.
    :param sensors:
    :param weekday:
    :param distance:
    :return:
    """
    response = RoadSituation(day=weekday, situation=[], hours=24)
    number_sensors = len(sensors)
    for hour in range(24):
        low = 0
        high = 0
        average = 0
        for sensor in sensors:
            sensor_id = sensor.id
            day_sensor = DaySensor.objects.get(sensor_id=sensor_id, day=weekday)
            instance = HourlyRoadSituation.objects.get(day_sensor_id=day_sensor.id, hour=hour)
            low += instance.low
            high += instance.high
            average += instance.average
        low = int(int(low / number_sensors)*distance)
        high = int(int(high / number_sensors)*distance)
        average = int(int(average / number_sensors)*distance)
        hourlySituation = OneHourRoadSituation(hour=hour, high=high, low=low, average=average)
        response.situation.append(hourlySituation)
    return response

def getRoadSituationData(sensors,distance):
    """
    based on related sensors and distance,return data at today and tomorrow.
    :param sensors:
    :param distance:
    :return:
    """
    weekday = datetime.now().weekday()
    today = getWeekDay(weekday)
    if today == 'sunday':
        tomorrow = 'monday'
    else:
        tomorrow = getWeekDay(weekday+1)
    today = getSituationList(sensors,today,distance)
    today.situation = [i.__dict__ for i in today.situation]
    tomorrow = getSituationList(sensors,tomorrow,distance)
    tomorrow.situation = [i.__dict__ for i in tomorrow.situation]
    return [today,tomorrow]


@require_GET
@valid_request
def getRoadSituation(request):
    """
    handle get road risk situation request
    :param request:
    :return:
    """
    if request.method == 'GET':
        user_lat = float(request.GET.get('user_lat',default=0))
        user_long = float(request.GET.get('user_long',default=0))
        gym_id = request.GET.get('gym_id',default=0)
        gym = Gym.objects.get(pk = gym_id)
        distance = haversine(gym.gym_coordinate_lat,gym.gym_coordinate_long,user_lat,user_long)
    else:
        return HttpResponseNotFound()
    if user_lat == 0 or user_long == 0 or gym_id == 0:
        return HttpResponseNotFound()
    sensor_list = findAllRelatedSensor(gym.gym_coordinate_lat,gym.gym_coordinate_long,user_lat,user_long)
    result = getRoadSituationData(sensor_list,distance)

    return HttpResponse(json.dumps({'list':[i.__dict__ for i in result]}),content_type='application/json')