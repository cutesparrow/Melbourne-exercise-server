from django.db import models
from gym.models import *
# Create your models here.
class LastHourSensor(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    situation = models.FloatField()

class PopularJoggingPath(models.Model):
    name = models.CharField(max_length=50)
    map = models.CharField(max_length=1000)
    distance = models.FloatField()
    elevation = models.FloatField()
    background = models.CharField(max_length=50)
    intruduction = models.TextField()
    suburb = models.CharField(max_length=50)
    postcode = models.CharField(max_length=10)
    latitude = models.FloatField()
    longitude = models.FloatField()
    detail_text = models.TextField()
    safety_tips = models.TextField()