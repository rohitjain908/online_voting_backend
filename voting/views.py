from turtle import position
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Voter, Votes
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

## id -1 is admin
## id - 2 is voter


@csrf_exempt
def deleteVoter(request):##request only admin can send
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request",
           
        })
    
    body = json.lodas(request.body)
    voterId = body['voterId']
    adminUniversity = body['adminUniversity']
    if not Voter.objects.filter(id = voterId).exists():
        return JsonResponse({
            "messgae" : "Failed",
            'text' : "Voter not exist"
        })


    voterInstance =  Voter.objects.get(id = voterId)
    voterUniversity = voterInstance.university

    if adminUniversity != voterUniversity:
        return JsonResponse({
            "messgae" : "Failed",
            'text' : "You can't delete this voter ,it's not belong to your university"
        })

    voterInstance.delete()

    return JsonResponse({
            "messgae" : "success",
            'text' : "deleted"
        })

    


    

@csrf_exempt
def editVoter(request):
    if request.method != 'POST':
        return JsonResponse({
            "message" : "This is not a Post request",
           
        })

    body = json.loads(request.body)
    voterId = body['voterId']

    if not Voter.objects.filter(id = voterId).exists():
        return JsonResponse({
            "message" : "Failed",
            'text' : "Voter not exist"
        })


    
    fullName = body['fullName']
    email = body['email']
    
    Voter.objects.filter(id = voterId).update(
        fullName = fullName,
        email = email,
    )

    return JsonResponse({
            "message" : "success",
            'text' : "Updated"
        })


    

@csrf_exempt
def votesList(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })


    body = json.loads(request.body)
    adminUniversity = body['adminUniversity']

    print(adminUniversity)
    

    votes = Votes.objects.all()
    votesList = []
    for vote in votes:
        if vote.voter.university != adminUniversity:
            continue

        if vote.candidate.university != adminUniversity:
            continue

        if vote.position.university != adminUniversity:
            continue

        voter = vote.voter.fullName
        candidate = vote.candidate.fullName
        position = vote.position.name

        votesList.append({
            'voter' : voter,
            'candidate' : candidate,
            'position' : position
        })

    
    return JsonResponse({
            "messgae" : "success",
            'votesList' : votesList
        })

@csrf_exempt
def voterList(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })


    body = json.loads(request.body)
    adminUniversity = body['adminUniversity']

    validVoter = Voter.objects.all().filter(university = adminUniversity)
    voterList = []

    for voter in validVoter:
        voterList.append({
            'id' : voter.id,
            'fullName' : voter.fullName,
            'email' : voter.email
        })


    return JsonResponse({
            "messgae" : "success",
            'voterList' : voterList
        })

@csrf_exempt
def getVoter(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    print(body)
    voterId = body['voterId']
    if not Voter.objects.all().filter(id = voterId).exists():
        return JsonResponse({
            "messgae" : "Failed",
            'text' : "Voter does not exist"
        })
    

    voter = Voter.objects.get(id = voterId)
    fullName = voter.fullName
    email = voter.email

    data = {
        "fullName" : fullName,
        "email" : email
    }

    return JsonResponse({
        "message" : "success",
        "data" : data
    })


    







