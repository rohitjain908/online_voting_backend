from ast import mod
from django.db import models


# Create your models here.

class User(models.Model):
    fullName = models.CharField(max_length = 100)
    password = models.CharField(max_length= 100)
    email = models.EmailField()
    isSuperAdmin = models.BooleanField()








