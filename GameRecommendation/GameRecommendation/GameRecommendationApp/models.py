from django.db import models

# Create your models here.\

class Rating(models.Model):
    userId = models.IntegerField()
    AppID = models.IntegerField()
    rating = models.IntegerField()

class PersonalRCM(models.Model):
    userId = models.IntegerField()
    rcmlist = models.TextField()
