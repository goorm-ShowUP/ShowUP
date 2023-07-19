from django.db import models

# Create your models here.
class Choice(models.Model):
    price = models.IntegerField(default = 10000)
    genre = models.CharField(max_length=100,default='classic')
    age = models.IntegerField(default = 20)
    runtime =models.IntegerField(default = 100)
    day = models.IntegerField(default = 3)

