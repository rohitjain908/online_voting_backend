from ast import mod
from django.db import models


# Create your models here.

class User(models.Model):
    fullName = models.CharField(max_length = 100)
    password = models.CharField(max_length= 100)
    email = models.EmailField()
    isSuperAdmin = models.BooleanField()

    def __str__(self):
        return self.email




class Admin(User):
    university = models.CharField(max_length = 100)

