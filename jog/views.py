from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json

from django.views.decorators.http import require_GET
from gym.views import valid_request
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
