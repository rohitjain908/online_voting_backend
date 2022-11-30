from operator import pos
from turtle import position
from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import Candidate, Position, Voter, Votes
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
    
    body = json.loads(request.body)
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
            'error' : "Voter not exist"
        })


    
    fullName = body['fullName']
    email = body['email']

    if Voter.objects.all().filter(email = email).exists():
        voter = Voter.objects.all().filter(email = email)[0]
        print("edit voter ")
        if voter.id != voterId:
            return JsonResponse({
                "message" : "Failed",
                'error' : "User with this email id already exist"
            })

    
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


@csrf_exempt
def candidatesList(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    adminUniversity = body['adminUniversity']
    validCandidates = Candidate.objects.all().filter(university = adminUniversity)
    candidatesList = []
    for candidate in validCandidates:
        if candidate.university != adminUniversity:
            continue
    
        candidatesList.append({
            "id" : candidate.id,
            "fullName" : candidate.fullName,
            "position" : candidate.position.name,
            "bio" : candidate.bio
        })

    print(candidatesList)

    return JsonResponse({
        "message" : "success",
        "candidatesList" : candidatesList
    })

@csrf_exempt
def addCandidate(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    fullName = body['fullName']
    bio = body['bio']
    positionId = body['positionId']
    university = body['university']

    if not Position.objects.all().filter(id = positionId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "this position doesn't exist, Please select valid position"
    })

    position = Position.objects.get(id = positionId)

    if Candidate.objects.all().filter(fullName = fullName).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "This candidate's name already exist, Please use some other name"
    })


    Candidate.objects.create(
        fullName = fullName,
        bio = bio,
        position = position,
        university = university
    )

    return JsonResponse({
            "message" : "success",
            "text" : "Added"
    })

@csrf_exempt
def positionsList(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    adminUniversity = body['adminUniversity']
    validPositions = Position.objects.all().filter(university = adminUniversity)
    postionsList = []
    
    for position in validPositions:
        totalVotes = len(Votes.objects.all().filter(position = position))
        #print(totalVotes)
        postionsList.append({
            "id" : position.id,
            "name" : position.name,
            "maxCandidates" : position.maxCandidates,
            "totalVotes" : totalVotes
        })

    return JsonResponse({
        "message" : "success",
        "postionsList" : postionsList
    })


@csrf_exempt
def getCandidate(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    candidateId = body['candidateId']

    if not Candidate.objects.filter(id = candidateId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "This candidate does not exist"
        })

    candidate = Candidate.objects.get(id = candidateId)

    data = {
        "fullName" : candidate.fullName,
        "bio" : candidate.bio,
        "position" : candidate.position.name,
        "positionId" : candidate.position.id
    }

    return JsonResponse({
        "message" : "success",
        "data" : data
    })
    


    

    
@csrf_exempt
def editCandidate(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    candidateId = body['candidateId']

    if not Candidate.objects.filter(id = candidateId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "This candidate does not exist"
        })

    fullName = body['fullName']
    bio = body['bio']
    positionId = body['positionId']
    university = body['university']


    if not Position.objects.all().filter(id = positionId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "this position doesn't exist, Please select valid position"
    })

    position = Position.objects.get(id = positionId)

    if Candidate.objects.all().filter(fullName = fullName).exists():
        id = Candidate.objects.all().filter(fullName = fullName)[0].id

        if id != candidateId:
            return JsonResponse({
                "message" : "Failed",
                "error" : "This candidate's name already exist, Please use some other name"
    })

    Candidate.objects.all().filter(id = candidateId).update(
        fullName = fullName,
        bio = bio,
        position = position,
        university = university
    )

    return JsonResponse({
        "message" : "success",
        "text" : "Update Candidate details"
    })



@csrf_exempt
def deleteCandidate(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    candidateId = body['candidateId']

    if not Candidate.objects.all().filter(id = candidateId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "Candidate does not exist"
    })
    
    instance = Candidate.objects.get(id = candidateId)
    instance.delete()

    return JsonResponse({
        "message" : "success",
        "text" : "Deleted"
    })

@csrf_exempt
def ballotPosition(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    adminUniversity = body['adminUniversity']

    validCandidates = Candidate.objects.all().filter(university = adminUniversity)
    ballotPosition = dict()
    for candidate in validCandidates:
        position = candidate.position.name
        ballotPosition[position] = []


    for candidate in validCandidates:
        position = candidate.position.name
        votes = len(Votes.objects.all().filter(candidate = candidate, position = candidate.position))
        ballotPosition[position].append({
            "name" : candidate.fullName,
            "bio" : candidate.bio,
            "votes" : votes
        })

    return JsonResponse({
        "message" : "success",
        "data" : ballotPosition
    })

@csrf_exempt
def addPosition(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    name = body['name']
    maxCandidates = body['maxCandidates']
    university = body['university']

    if Position.objects.all().filter(university = university , name = name).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "This position already exits, please use some other name"
        })

    
    Position.objects.create(
        name = name,
        maxCandidates = maxCandidates,
        university = university
    )


    return JsonResponse({
        "message" : "success",
        "text" : "Created"
    })


@csrf_exempt
def getPosition(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    positionId = body['positionId']

    if not Position.objects.filter(id = positionId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "This Position does not exist"
        })

    position = Position.objects.get(id = positionId)

    positionDetail = {
        "name" : position.name,
        "maxCandidates" : position.maxCandidates
    }

    return JsonResponse({
        "message" : "success",
        "positionDetail" : positionDetail
    })


@csrf_exempt
def editPosition(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    positionId = body['positionId']

    if not Position.objects.all().filter(id = positionId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "This position does not exist"
        })

    name = body['name']
    maxCandidates = body['maxCandidates']
    university = body['university']

    if Position.objects.all().filter(name = name , university = university):
        id = Position.objects.all().filter(name = name, university = university)[0].id

        if id != positionId:
            return JsonResponse({
                "message" : "Failed",
                "error" : "this position already exist , please use some other name"
            })
    
    Position.objects.all().filter(id = positionId).update(
        name = name,
        maxCandidates = maxCandidates,
        university = university
    )

    return JsonResponse({
        "message" : "success",
        "text" : "Update Position details"
    })


@csrf_exempt
def deletePosition(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    positionId = body['positionId']

    if not Position.objects.all().filter(id = positionId).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "Position does not exist"
    })
    
    instance = Position.objects.get(id = positionId)
    instance.delete()

    return JsonResponse({
        "message" : "success",
        "text" : "Deleted"
    })


@csrf_exempt
def getDashBoardData(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    adminUniversity = body['adminUniversity']


    votes = 0
    validCandidates = Candidate.objects.all().filter(university = adminUniversity)
    for candidate in validCandidates:
        votes = votes + len(Votes.objects.all().filter(candidate = candidate))
    candidates = len(Candidate.objects.all().filter(university = adminUniversity))
    positions = len(Position.objects.all().filter(university = adminUniversity))
    voters = len(Voter.objects.all().filter(university = adminUniversity))

    dashBoardData = {
        "votes" : votes,
        "voters" : voters,
        "positions" : positions,
        "candidates" : candidates
    }

    return JsonResponse({
        "message" : 'success',
        "dashBoardData" : dashBoardData
    })

@csrf_exempt
def isVoted(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    voterId = body['voterId']

    if not Voter.objects.all().filter(id = voterId).exists():
        return JsonResponse({
            "message" : 'Failed',
            "error" : "Voter does not exist"
    })


    voted = Voter.objects.get(id = voterId).voted
    return JsonResponse({
            "message" : 'success',
            "voted" : voted
    })

@csrf_exempt
def voterBallot(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    voterId = body['voterId']

    if not Voter.objects.all().filter(id = voterId).exists():
        return JsonResponse({
            "message" : 'Failed',
            "error" : "Voter does not exist"
    })

    voter = Voter.objects.get(id = voterId)
    votes = Votes.objects.all().filter(voter = voter)

    ballot = {}

    for vote in votes:
        candidate = vote.candidate
        position = vote.position

        ballot[position.name] = candidate.fullName

    
    return JsonResponse({
            "message" : 'success',
            "ballot" : ballot
    })

@csrf_exempt
def submitBallot(request):
    if request.method != 'POST':
        return JsonResponse({
            "messgae" : "This is not a Post request"
        })

    body = json.loads(request.body)
    voterId = body['voterId']
    votes = body['votes']

    voter = Voter.objects.get(id = voterId)
    university = voter.university
    print(votes)
    for positionName in votes:
        candidatename = votes[positionName]
        candidate = Candidate.objects.get(university = university, fullName = candidatename)
        position = Position.objects.get(name = positionName, university = university)

        Votes.objects.create(
            voter = voter,
            position = position,
            candidate = candidate
        )


    Voter.objects.all().filter(id = voterId).update(
        voted = True
    )
    return JsonResponse({
        "message" : 'success',    
    })
    

    



    


    











        

    

     

    





    







    







