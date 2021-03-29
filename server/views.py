from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
import json
import os
from random import choice
from gym.models import *
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

def safePolicy(request):
    safe_policy_list = list(SafetyPolicy.objects.all())
    result_list = []
    for i in safe_policy_list:
        safe_policy = SafePolicy(id=i.id,date=i.start_date,title=i.title,content=i.content)
        result_list.append(safe_policy)
    return HttpResponse(json.dumps([i.__dict__ for i in result_list]),content_type='application/json')



def exerciseTips(request):
    exercise_tips_list = list(ExerciseTips.objects.all())
    result = choice(exercise_tips_list)
    return HttpResponse(result.content)

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
