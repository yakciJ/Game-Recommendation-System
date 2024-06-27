from django.db import models

# Create your models here.\

class Rating(models.Model):
    userId = models.IntegerField()
    AppID = models.IntegerField()
    rating = models.IntegerField()
