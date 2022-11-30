from django.db import models
from user.models import User
from django.db.models.fields.related import ForeignKey
from django.db.models.deletion import CASCADE



class Voter(User):
    voted = models.BooleanField()
    university = models.CharField(max_length = 100)


class Position(models.Model):
    name = models.CharField(max_length = 100)
    university = models.CharField(max_length = 100)
    maxCandidates = models.IntegerField()

    def __str__(self):
        return self.name


#a candidate can be a voter
class Candidate(models.Model):
    fullName = models.CharField(max_length = 100)
    #ballotNumber = models.IntegerField() # assume:- ballot number will be candidate id
    position = ForeignKey(Position, on_delete = CASCADE)
    bio = models.CharField(max_length = 100)
    university = models.CharField(max_length = 100, default = "public university")
    #profile_pic = models.ImageField()
    #voters = models.ManyToManyField(Voter)


    def __str__(self):
        return self.fullName
    

class Votes(models.Model):
    voter = ForeignKey(Voter, on_delete = CASCADE)
    position = ForeignKey(Position, on_delete = CASCADE)
    candidate = ForeignKey(Candidate, on_delete = CASCADE)

