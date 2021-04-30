from django.db import models


from enum import Enum



class WeekDay(Enum):
    monday = "Mon"
    tuesday = "Tue"
    wednesday = "Wed"
    thursday = "Thu"
    friday = "Fri"
    saturday = "Sat"
    sunday = "Sun"
# Create your models here.
class Gym(models.Model):
    gym_name = models.CharField(max_length=30)
    gym_address = models.CharField(max_length=80)
    gym_limitation = models.IntegerField(default=0)
    gym_coordinate_lat = models.FloatField()
    gym_coordinate_long = models.FloatField()
    gym_class = models.CharField(max_length=40)
    def __str__(self):
        return self.gym_name

class Image(models.Model):
    gym = models.ForeignKey(Gym,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=10)
    def __str__(self):
        return self.image_name + ' ' + self.gym.gym_name

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=10)

class SafeTips(models.Model):
    exercise = models.ForeignKey(Exercise,on_delete=models.CASCADE)
    content = models.CharField(max_length=200)
    def __str__(self):
        return self.content

class ExerciseTips(models.Model):
    exercise = models.ForeignKey(Exercise,on_delete=models.CASCADE)
    content = models.CharField(max_length=20)

class SafetyPolicy(models.Model):
    start_date = models.CharField(max_length=12)
    title = models.CharField(max_length=50)
    content = models.CharField(max_length=1000)

class AboutCovid(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    background = models.CharField(max_length=50)
    color = models.CharField(max_length=20)

class Park(models.Model):
    park_name = models.CharField(max_length=30)
    park_address = models.CharField(max_length=80)
    park_coordinate_lat = models.FloatField()
    park_coordinate_long = models.FloatField()
    def __str__(self):
        return self.park_name

class ParkImage(models.Model):
    park = models.ForeignKey(Park,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=10)
    def __str__(self):
        return self.image_name + ' ' + self.park.park_name

class Playground(models.Model):
    playground_name = models.CharField(max_length=30)
    playground_address = models.CharField(max_length=80)
    playground_coordinate_lat = models.FloatField()
    playground_coordinate_long = models.FloatField()
    def __str__(self):
        return self.playground_name

class PlaygroundImage(models.Model):
    playground = models.ForeignKey(Playground,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=10)
    def __str__(self):
        return self.image_name + ' ' + self.playground.playground_name

class Sensor(models.Model):
    sensor_coordinate_lat = models.FloatField()
    sensor_coordinate_long = models.FloatField()
    sensor_name = models.CharField(max_length=20)

class DaySensor(models.Model):
    sensor = models.ForeignKey(Sensor,on_delete=models.CASCADE)
    day = models.CharField(max_length=3,choices=[(tag.value,tag.name) for tag in WeekDay])
    hours = models.IntegerField()

class HourlyRoadSituation(models.Model):
    day_sensor = models.ForeignKey(DaySensor,on_delete=models.CASCADE)
    hour = models.IntegerField()
    high = models.IntegerField()
    low = models.IntegerField()
    average = models.IntegerField()

class ExerciseBenefits(models.Model):
    content = models.CharField(max_length=200)
