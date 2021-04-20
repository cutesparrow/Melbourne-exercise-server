from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
from gym.models import *
from django.views.decorators.http import require_GET
from gym.views import valid_request
from jog.models import LastHourSensor,PopularJoggingPath
import requests
from gym.views import haversine
import math
import polyline
import shutil
import random
from multiprocessing.pool import ThreadPool
from django.conf import settings as django_settings
import os
import uuid
import sys
from django.contrib.staticfiles.storage import staticfiles_storage
from mapbox import encoding
import urllib
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
    length = float(request.GET.get('length',default=0))*1000
    type = request.GET.get('type')
    # pathPlanListCollections = selectFourPoint(user_latitude=lat,user_longitude=long,length=length)
    # count = min(7,len(pathPlanListCollections))
    # if count != 1:
    #     count = random.randint(1, count)
    # else:
    #     count = 1
    # pathPlanListCollections = random.choices(pathPlanListCollections,k=count)
    # size = len(pathPlanListCollections)
    # pool = ThreadPool(size)
    # resultList = pool.map(getPathFromAPI,pathPlanListCollections)
    # pool.close()
    # pool.join()

    responseList = []
    seeds = [random.randint(1,sys.maxsize) for i in range(1,10)]
    imageNameList = [str(uuid.uuid4())+'.png' for i in range(1,10)]
    input = [[lat,long,length,seeds[i],imageNameList[i],type] for i in range(len(seeds))]
    size = len(seeds)
    pool = ThreadPool(size)
    resultList = pool.map(getRouteFromAPI,input)
    pool.close()
    pool.join()
    id = 0
    for i in resultList:
        if i is None:
            continue
        responseList.append(CustomizedCard(id=id,image=i[3],distance=i[1],risk=i[4],time=str(i[2])+' min',instructions=i[0]))
        id += 1

    return HttpResponse(json.dumps([i.__dict__ for i in responseList]),content_type='application/json')

def getRouteFromAPI(input):
    lat = round(float(input[0]),9)
    long = round(float(input[1]),9)
    length = input[2]
    seed = input[3]
    imageName = input[4]
    type = input[5]
    baseURL = "https://graphhopper.com/api/1/route"
    point = (lat,long)
    algorithm = 'round_trip'
    distance = length
    key = "7a1ae47b-802e-4bc9-ab1d-a36dcaf05720"
    requestURL = baseURL + "?point=" + str(point[0]) + ',' + str(
        point[1]) + "&vehicle="+type+"&ch.disable=true&algorithm=" + algorithm + "&round_trip.distance=" + str(
        distance) + "&round_trip.seed=" + str(seed) + "&points_encoded=false" + "&key=" + key
    res = requests.get(requestURL)
    try:
        coordinatesList = json.loads(res.text)['paths'][0]['points']['coordinates']
    except KeyError as e:
        # print(requestURL)
        # print(e)
        return
    realDistance = round(int(json.loads(res.text)['paths'][0]['distance'])/1000,1)
    time = round(json.loads(res.text)['paths'][0]['time']/60000,1)
    instructionsList = []
    for i in json.loads(res.text)['paths'][0]['instructions'][1:]:
        if i["distance"] != 0:
            instructionsList.append(i["text"] + " and walk for " + str(round(i['distance'], 1)) + 'm')
    instructionsList.append("Finish")
    if type == 'foot':
        risk = assessRisk(coordinatesList)
        color = getColor(risk)
    else:
        risk = 'low'
        color = '0061ff'
    encodedCoordinatesList = encoding.encode_polyline(coordinatesList)
    encodedCoordinatesList = urllib.parse.quote(encodedCoordinatesList,safe='')
    requestUrl = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-s+ff2600("+str(long)+","+str(lat)+"),"+"path-3+"+color+"-0.85(" + encodedCoordinatesList +")/auto/300x200@2x?access_token=pk.eyJ1IjoiZ2FveXVzaGkwMDEiLCJhIjoiY2tubGM0cmV1MGY5aTJucGVtMHAwZGtpNyJ9.xApcEalgtGPF4fQc4to1DA"
    res = requests.get(requestUrl)
    if res.status_code != 200:
        return
    with staticfiles_storage.open(os.path.join(django_settings.STATIC_ROOT, imageName), 'wb') as out_file:
        out_file.write(res.content)
    del res
    return instructionsList,realDistance,time,imageName,risk

def getColor(risk):
    if risk == 'high':
        return 'ff2600'
    elif risk == 'mid':
        return 'cc6600'
    elif risk == 'low':
        return 'cc9933'
    else:
        return '33ff00'
def assessRisk(coordinates):
    number = calculateRisk(coordinates)
    if number > 40:
        return 'high'
    elif number > 30:
        return 'mid'
    elif number > 20:
        return 'low'
    else:
        return 'no'

def calculateRisk(coordinates):
    start = coordinates[0]
    far = coordinates[int(len(coordinates)/2)]
    big_lat,small_lat = max(start[1],far[1]),min(start[1],far[1])
    big_long,small_long = max(start[0],far[0]),min(start[0],far[0])
    sensor_list = Sensor.objects.filter(sensor_coordinate_lat__gte = small_lat,
                                        sensor_coordinate_lat__lte = big_lat,
                                        sensor_coordinate_long__gte = small_long,
                                        sensor_coordinate_long__lte = big_long)
    sensor_list = list(sensor_list)
    situationList = []
    for i in sensor_list:
        try:
            nowSituation = LastHourSensor.objects.get(sensor_id=i.id)
            situationList.append(int(nowSituation.situation))
        except:
            pass
    if len(situationList) == 0:
        lat = (big_lat+small_lat)/2
        long = (big_long+small_long)/2
        distance = 2**31
        close_sensor = None
        for i in Sensor.objects.all():
            check = LastHourSensor.objects.filter(sensor_id=i.id)
            if haversine(long,lat,i.sensor_coordinate_long,i.sensor_coordinate_lat) < distance and check.exist():
                close_sensor = i.id

        situationList.append(int(LastHourSensor.objects.get(sensor_id=close_sensor).situation))
    return sum(situationList)/len(situationList)


def getPopularCardList(allPopularPath,userLat,userLong):
    popularPathList = []
    size = len(allPopularPath)
    pool = ThreadPool(size)
    input = [[i.map, i.latitude, i.longitude] for i in allPopularPath]
    resultList = pool.map(getMapImage,input)
    for i in range(len(allPopularPath)):
        distanceToUser = round(haversine(float(userLong),float(userLat),float(allPopularPath[i].longitude),float(allPopularPath[i].latitude)),1)
        imageName = resultList[i]
        card = PopularCard(id=i,name=allPopularPath[i].name,map=imageName,distance=distanceToUser,longth=allPopularPath[i].distance,elevation=allPopularPath[i].elevation,background=allPopularPath[i].background,intruduction=allPopularPath[i].intruduction,suburb=allPopularPath[i].suburb,postcode=allPopularPath[i].postcode,detail_text=allPopularPath[i].detail_text,lat=allPopularPath[i].latitude,long=allPopularPath[i].longitude)
        popularPathList.append(card)


    return popularPathList

def getMapImage(input):
    path = input[0]
    lat = input[1]
    long = input[2]
    encodedCoordinatesList = urllib.parse.quote(path, safe='')
    requestUrl = "https://api.mapbox.com/styles/v1/mapbox/streets-v11/static/pin-s+ff2600(" + str(long) + "," + str(
        lat) + ")," + "path-3+0061ff-0.55(" + encodedCoordinatesList + ")/auto/300x200@2x?access_token=pk.eyJ1IjoiZ2FveXVzaGkwMDEiLCJhIjoiY2tubGM0cmV1MGY5aTJucGVtMHAwZGtpNyJ9.xApcEalgtGPF4fQc4to1DA"
    res = requests.get(requestUrl)
    imageName = str(uuid.uuid4())+'.png'
    with staticfiles_storage.open(os.path.join(django_settings.STATIC_ROOT, imageName), 'wb') as out_file:
        out_file.write(res.content)
    del res
    return imageName


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

def selectFourPoint(user_latitude,user_longitude,length):
    with open('./jog/coordinates.json') as json_file:
        data = eval(json_file.read())
    interesections = data
    farPoints = []
    length = float(length)
    for i in range(len(interesections)):
        for j in range(len(interesections[i])):
            distance = haversine(float(user_longitude),float(user_latitude),float(interesections[i][j][1]),float(interesections[i][j][0]))
            if distance > length/(2*math.sqrt(2)) - length/10 and distance < length/(2*math.sqrt(2))+ length/10:
                farPoints.append(Coordinate(latitude=interesections[i][j][0],longitude=interesections[i][j][1]))
    pointPaire = []
    for i in farPoints:
        potential = []
        for m in interesections:
            for n in m:
                distance1 = haversine(float(user_longitude),float(user_latitude),float(n[1]),float(n[0]))
                distance2 = haversine(i.longitude,i.latitude,n[1],n[0])
                if distance1 > length/4 - length/10 and distance1 < length/4 + length/10 and distance2 > length/4 - length/10 and distance2 < length/4 + length/10:
                    potential.append(Coordinate(latitude=n[0],longitude=n[1]))
        for i in range(1,len(potential)):
            distance = haversine(potential[0].longitude,potential[0].latitude,potential[i].longitude,potential[i].latitude)
            if distance > length/(2*math.sqrt(2)) - length/10 and distance < length/(2*math.sqrt(2))+ length/10:
                pointPaire.append((potential[0],potential[i]))
                break
    count = min(len(farPoints),len(pointPaire))
    resultList = []
    for i in range(count):
        star =  Coordinate(latitude=float(user_latitude),longitude=float(user_longitude))
        far = farPoints[i]
        front = pointPaire[i][0]
        back = pointPaire[i][1]
        resultList.append((star,front,far,back))

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
    def __init__(self,id,image,distance,risk,time,instructions):
        self.id = id
        self.image = image
        self.distance = distance
        self.risk = risk
        self.time = time
        self.instructions = instructions

class PopularCard:
    def __init__(self,id,name,map,lat,long,distance,longth,elevation,background,intruduction,suburb,postcode,detail_text):
        self.id = id
        self.name = name
        self.map = map
        self.distance = distance
        self.longth = longth
        self.elevation = elevation
        self.background = background
        self.intruduction = intruduction
        self.suburb = suburb
        self.postcode = postcode
        self.latitude = lat
        self.longitude = long
        self.detail_text = detail_text

class Coordinate:
    def __init__(self,latitude,longitude):
        self.latitude = latitude
        self.longitude = longitude
