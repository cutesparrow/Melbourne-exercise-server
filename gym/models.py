from django.db import models

# Create your models here.
class Gym(models.Model):
    gym_name = models.CharField(max_length=30)
    gym_address = models.CharField(max_length=80)
    gym_limitation = models.IntegerField(default=0)
    gym_coordinate_lat = models.FloatField()
    gym_coordinate_long = models.FloatField()
    def __str__(self):
        return self.gym_name

class Image(models.Model):
    gym = models.ForeignKey(Gym,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=10)
    def __str__(self):
        return self.image_name + ' ' + self.gym.gym_name
