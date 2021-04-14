from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
from gym.models import *
from django.views.decorators.http import require_GET
from gym.views import valid_request
from jog.models import LastHourSensor,PopularJoggingPath
import requests
from gym.views import haversine
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
    allPopularJoggingPath = PopularJoggingPath.objects.all()
    userLat = request.GET.get('lat',default=0)
    userLong = request.GET.get('long',default=0)
    result = getPopularCardList(allPopularJoggingPath,userLat,userLong)
    return HttpResponse(json.dumps([i.__dict__ for i in result]),content_type='application/json')

@require_GET
@valid_request
def customizedCards(request):
    lat = request.GET.get('lat',default=0)
    long = request.GET.get('long',default=0)
    pathPlanList = selectFourPoint(user_latitude=lat,user_longitude=long)
    pathPointList,directions,distance = getPathFromAPI(pathPlanList)
    response = [CustomizedCard(id=1,path=pathPointList,distance=round(distance/1000,1),risk="low",time=str(round(distance*5/1000)) + ' Min',directions=directions)]
    return HttpResponse(json.dumps([i.__dict__ for i in response]),content_type='application/json')

def getPopularCardList(allPopularPath,userLat,userLong):
    id = 0
    popularPathList = []
    for i in allPopularPath:
        pathList = eval(i.path)
        path = []
        for j in pathList:
            path.append(Coordinate(latitude=j[0],longitude=j[1]))
        risk = calculateRisk(path)
        central = eval(i.centralPoint)
        distanceToUser = round(haversine(float(userLong),float(userLat),float(central[1]),float(central[0])),1)
        card = PopularCard(id=id,path=path,distance=i.distance,risk=risk,time=str(i.time)+' Min',popularStar=i.popularStar,distanceToUser=distanceToUser)
        popularPathList.append(card)
    return popularPathList


def calculateRisk(path):
    # calculate the risk level based on the path
    return 'low'

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
    directions = []
    distance = 0
    for i in result['routes'][0]['legs']:
        distance += i['distance']['value']
        for j in i['steps']:
            directions.append(j['html_instructions'])
            pathCoordinateList.append(Coordinate(latitude=j['end_location']['lat'],longitude=j['end_location']['lng']))
    pathCoordinateList.insert(0,Coordinate(latitude=float(pathCoordinateList[-1].latitude),longitude=float(pathCoordinateList[-1].longitude)))
    return pathCoordinateList,directions,distance

def selectFourPoint(user_latitude,user_longitude):
    resultList = []
    startPoint = Coordinate(latitude=float(user_latitude),longitude=float(user_longitude))
    farPoint = Coordinate(latitude=-37.81013712756485, longitude=144.9696444596486)
    frontPoint = Coordinate(latitude=-37.81225616712328, longitude=144.96224156339468)
    backPoint = Coordinate(latitude=-37.8072551361701, longitude=144.9683140840899)
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
    def __init__(self,id,path,distance,risk,time,directions):
        self.id = id
        self.path = [i.__dict__ for i in path]
        self.distance = distance
        self.risk = risk
        self.time = time
        self.directions = directions

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
