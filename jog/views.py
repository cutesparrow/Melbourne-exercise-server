from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
from gym.models import *
from django.views.decorators.http import require_GET
from gym.views import valid_request
from jog.models import LastHourSensor
import requests
# Create your views here.


@require_GET
@valid_request
def index(request):
    return HttpResponse("Hello, please download our appication")

@require_GET
@valid_request
def path(request):
    if request.method == "GET":
        lat = request.GET.get('lat',default = 0)
        long = request.GET.get('long',default = 0)
        ifreturn = request.GET.get('ifreturn',default = 'False')
    response = [{
        "longitude":144.95963315775296,
            "latitude":-37.80912284071033},
                 {
                     "longitude":144.9825356942,
                     "latitude":-37.8452163566
                 }]

    if ifreturn == 'True' or ifreturn == 'False':
        return HttpResponse(json.dumps(response),content_type='application/json')
    else:
        return HttpResponseNotFound('error input')


@require_GET
@valid_request
def sensorSituation(request):
    allSensorSituation = LastHourSensor.objects.all()
    result = responseSensorSituationList(allSensorSituation)
    return HttpResponse(json.dumps([i.__dict__ for i in result]),content_type='application/json')


def responseSensorSituationList(allSensorSituation):
    sensorList = []
    id = 0
    for i in allSensorSituation:
        sensorList.append(ResponseSensorSituation(id=id,sensorSituation=i))
        id += 1
    return sensorList

@require_GET
@valid_request
def popularCards(request):
    pass

@require_GET
@valid_request
def customizedCards(request):
    lat = request.GET.get('lat',default=0)
    long = request.GET.get('long',default=0)
    pathPlanList = selectFourPoint(user_latitude=lat,user_longitude=long)
    pathPointList = getPathFromAPI(pathPlanList)
    response = [CustomizedCard(id=1,path=pathPointList,distance=5.2,risk="low",time="35min")]
    return HttpResponse(json.dumps([i.__dict__ for i in response]),content_type='application/json')

def getPathFromAPI(pointList):
    baseURL = "https://maps.googleapis.com/maps/api/directions/json"
    viaString = "&waypoints="
    for i in pointList[1:]:
        viaString += str(i.latitude) + '%2C' + str(i.longitude) + '%7C'
    viaString = viaString[:-3]
    res = requests.get(
        baseURL + "?origin=" + str(pointList[0].latitude) + ',' + str(pointList[0].longitude) + "&destination=" + str(
            pointList[0].latitude) + ',' + str(
            pointList[0].longitude) + "&key=" + "AIzaSyB58sfxyNZYcF91YPFHmD-iTvBja-LbBxE" + "&mode=walking" + viaString)
    result = json.loads(res.text)
    pathCoordinateList = []
    for i in result['routes'][0]['legs']:
        for j in i['steps']:
            pathCoordinateList.append(Coordinate(latitude=j['end_location']['lat'],longitude=j['end_location']['lng']))
    return pathCoordinateList

def selectFourPoint(user_latitude,user_longitude):
    resultList = []
    startPoint = Coordinate(latitude=user_latitude,longitude=user_longitude)
    farPoint = Coordinate(latitude=-37.80698388412978, longitude=144.9658893673459)
    frontPoint = Coordinate(latitude=-37.808848721785054, longitude=144.96631852075188)
    backPoint = Coordinate(latitude=-37.80817060445021, longitude=144.96033183073786)
    resultList.append(startPoint)
    resultList.append(frontPoint)
    resultList.append(farPoint)
    resultList.append(backPoint)
    return resultList


class ResponseSensorSituation:
    def __init__(self,id,sensorSituation):
        self.id = id
        currentSensor = Sensor.objects.get(pk=sensorSituation.sensor_id)
        self.lat = currentSensor.sensor_coordinate_lat
        self.long = currentSensor.sensor_coordinate_long
        self.risk = self.assessRiskLevel(sensorSituation.situation)

    def assessRiskLevel(self,number):
        if number <5:
            return 'no'
        elif number < 10:
            return 'low'
        elif number < 20:
            return 'medium'
        else:
            return 'high'

class CustomizedCard:
    def __init__(self,id,path,distance,risk,time):
        self.id = id
        self.path = [i.__dict__ for i in path]
        self.distance = distance
        self.risk = risk
        self.time = time

class PopularCard:
    def __init__(self,id,path,distance,risk,time,popularStar,distanceToUser):
        self.id = id
        self.path = [i.__dict__ for i in path]
        self.distance = distance
        self.risk = risk
        self.time = time
        self.popularStar = popularStar
        self.distanceToUser = distanceToUser

class Coordinate:
    def __init__(self,latitude,longitude):
        self.latitude = latitude
        self.longitude = longitude
