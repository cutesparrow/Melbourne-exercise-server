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
    return HttpResponse("fdsalkjfhksadjf;lksjd;flkj;slkdfasdkfj")

def safeTips(request):
    return HttpResponse("fkjdsahfglkjfdshlgjkhsdflkjghldsjfkhgljksdhflgjkhsdlfkjghlsjdfhgljkshdfljghsdlfjkghldsjkfhglkjsdfhljgkhdsfljkghldskjfhglkjsdfhlgjkhdsflkghldskf")