from django.db import models
from user.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import CASCADE

# Create your models here.

class Voter(User):
    voted = models.BooleanField()
    university = models.CharField(max_length = 100)


class Position(models.Model):
    name = models.CharField(max_length = 100)
    university = models.CharField(max_length = 100)
    maxVotes = models.IntegerField()


#a candidate can be a voter
class Candidate(models.Model):
    fullName = models.CharField(max_length = 100)
    ballotNumber = models.IntegerField()
    position = ForeignKey(Position, on_delete = CASCADE)
    bio = models.CharField(max_length = 100)
    #profile_pic = models.ImageField()
    voters = models.ManyToManyField(Voter)
    

class Votes(models.Model):
    voter = ForeignKey(Voter, on_delete = CASCADE)
    position = ForeignKey(Position, on_delete = CASCADE)
    candidate = ForeignKey(Candidate, on_delete = CASCADE)

