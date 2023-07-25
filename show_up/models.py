from django.db import models

# Create your models here.

class Show(models.Model):
    id = models.AutoField(primary_key=True)
    showname = models.CharField(max_length=200)		#공연명
    # showid = models.CharField(max_length=200)		#공연ID
    concerthall =models.CharField(max_length=200) # 공연장
    sido = models.CharField(max_length=200)	      # 지역(시도)
    gugun = models.CharField(max_length=200)	  #지역(구군)
    genre = models.CharField(max_length=200)
    price = models.IntegerField(null=True)
    age = models.IntegerField(null=True)
    runtime = models.IntegerField(null=True)
    period = models.IntegerField(null=True)
    cluster = models.IntegerField(null=True)
    
    