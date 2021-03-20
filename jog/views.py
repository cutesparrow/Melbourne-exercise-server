from django.shortcuts import render
from django.http import HttpResponse



# Create your views here.



def index(request):
    return HttpResponse("Hello, please download our appication")

def path(request):
    if request.method == "GET":
        lat = request.GET.get('lat',default = 0)
        long = request.GET.get('long',default = 0)
    return HttpResponse("Your location is "+lat+'  '+long )
