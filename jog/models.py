from django.db import models
from gym.models import *
# Create your models here.
class LastHourSensor(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    situation = models.FloatField()

class PopularJoggingPath(models.Model):
    pathName = models.CharField(max_length=20)
    path = models.CharField(max_length=2000)
    distance = models.FloatField()
    time = models.IntegerField()
    popularStar = models.IntegerField()
    centralPoint = models.CharField(max_length=50)