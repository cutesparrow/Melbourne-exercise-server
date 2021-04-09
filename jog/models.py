from django.db import models
from gym.models import *
# Create your models here.
class LastHourSensor(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    situation = models.FloatField()
