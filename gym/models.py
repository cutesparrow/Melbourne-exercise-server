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

class SafeTips(models.Model):
    topic = models.CharField(max_length=10)
    subTitle = models.CharField(max_length=30)
    content = models.CharField(max_length=200)
    def __str__(self):
        return self.topic

class Exercise(models.Model):
    exercise_name = models.CharField(max_length=10)

class ExerciseTips(models.Model):
    exercise = models.ForeignKey(Exercise,on_delete=models.CASCADE)
    content = models.CharField(max_length=20)


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

class playgroundImage(models.Model):
    playground = models.ForeignKey(Playground,on_delete=models.CASCADE)
    image_name = models.CharField(max_length=10)
    def __str__(self):
        return self.image_name + ' ' + self.playground.playground_name
