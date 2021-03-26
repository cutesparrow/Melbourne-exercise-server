from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
import os
from random import choice

def poster(request):
    fileList = file_name_listdir('./static')
    try:
        name = choice(fileList)
    except Exception as e:
        name = "error"
    return HttpResponse(name)

def file_name_listdir(file_dir):
    fileList = []
    for files in os.listdir(file_dir):
        fileList.append(files)
    fileListNew = []
    for i in range(len(fileList)):
        if fileList[i].startswith('poster'):
            fileListNew.append(fileList[i])
        else:
            pass
    return fileListNew
def slogan(request):
    return HttpResponse("Avoid the following situations: strained reps, poor energy levels, incomplete sets, longer-than-desired workouts, and shoddy results.")

def safeTips(request):
    return HttpResponse("""
Gyms and indoor recreation

Classes and group exercise classes may be held with up to 50 people and a maximum density of 1 person per 4 square metres. 
It is recommended that you wear a face mask when exercising indoors where you can’t keep 1.5 metre distance from others, except where that exercise or physical activity leaves you short of breath or puffing.""")