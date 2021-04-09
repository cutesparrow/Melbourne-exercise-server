from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
from gym.models import *
from django.views.decorators.http import require_GET
from gym.views import valid_request
from jog.models import LastHourSensor
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