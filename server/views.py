from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
import os
from random import choice
from gym.models import *
from random import choice
from functools import wraps
from gym.views import valid_request
from django.views.decorators.http import require_GET
from django.contrib.staticfiles.storage import staticfiles_storage
from django.conf import settings

@require_GET
@valid_request
def poster(request):
    fileList = file_name_listdir(settings.STATIC_URL)
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

@require_GET
@valid_request
def getClassedExerciseTips(request):
    exerciseTipsList = list(ExerciseClassedTip.objects.all())
    result_list = []
    id = 0
    for i in exerciseTipsList:
        tip = ResponseTip(id=id,content=i.content,tipClass=i.tipClass)
        result_list.append(tip)
        id += 1
    return HttpResponse(json.dumps([i.__dict__ for i in result_list]),content_type='application/json')

class ResponseTip:
    def __init__(self,content,id,tipClass):
        self.content = content
        self.id = id
        self.tipClass = tipClass

@require_GET
@valid_request
def safePolicy(request):
    safe_policy_list = list(SafetyPolicy.objects.all())
    result_list = []
    for i in safe_policy_list:
        safe_policy = SafePolicy(id=i.id,date=i.start_date,title=i.title,content=i.content)
        result_list.append(safe_policy)
    return HttpResponse(json.dumps([i.__dict__ for i in result_list]),content_type='application/json')

@require_GET
@valid_request
def aboutCovid19(request):
    about_covid_list = list(AboutCovid.objects.all())
    result_list = []
    for i in about_covid_list:
        about_covid = AboutCovidResponse(id=i.id,title=i.title,content=i.content,background=i.background,color=i.color)
        result_list.append(about_covid)
    return HttpResponse(json.dumps([i.__dict__ for i in result_list]),content_type='application/json')

@require_GET
@valid_request
def exerciseTips(request):
    exercise_tips_list = list(ExerciseTips.objects.all())
    result = choice(exercise_tips_list)
    return HttpResponse(result.content)

def homePage(request):
    return HttpResponse('Hello, this is the backend for our Melbourne safe exercise ios application.\n You can not access other content of this site if you don\'t have a valid access token.')

@require_GET
@valid_request
def safeTips(request):
    safe_tips_list = list(SafeTips.objects.all())
    result = choice(safe_tips_list)
    return HttpResponse(result.content)

class SafePolicy:
    def __init__(self,id,date,title,content):
        self.id = id
        self.date = date
        self.title = title
        self.content = content

class AboutCovidResponse:
    def __init__(self,id,title,content,background,color):
        self.id = id
        self.title = title
        self.content = content
        self.background = background
        self.color = color

@require_GET
@valid_request
def getShowsInformation(request):
    exercise_list = list(Exercise.objects.filter(exercise_name='gym'))
    exercise = choice(exercise_list)
    type = exercise.exercise_name
    type = 'gym'
    exerciseTipsList = exercise.exercisetips_set.all()
    safetyTipsList = exercise.safetips_set.all()
    exercise_tip = choice(list(exerciseTipsList)).content
    safety_tip = choice(list(safetyTipsList)).content
    image = getRelatedImage(type)
    benefit = choice(list(ExerciseBenefits.objects.all())).content
    response = ShowInformation(imageName=image,safetyTips=safety_tip,exerciseTips=exercise_tip,exerciseBenefits=benefit)
    return HttpResponse(json.dumps(response.__dict__),content_type='application/json')
def getRelatedImage(type):
    fileList = file_name_listdir(settings.STATIC_URL)
    if type == 'walk_dog':
        type = 'dog'
    newList = []
    for i in range(len(fileList)):
        if type in fileList[i]:
            newList.append(fileList[i])
    return choice(newList)

class ShowInformation:
    def __init__(self,imageName,safetyTips,exerciseTips,exerciseBenefits):
        self.imageName = imageName
        self.safetyTips = safetyTips
        self.exerciseTips = exerciseTips
        self.exerciseBenefits = exerciseBenefits



























