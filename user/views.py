from django.shortcuts import render, HttpResponse
import jwt, datetime
from rest_framework import exceptions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User
from voting.models import *
from django.contrib.auth.hashers import make_password,  check_password

# Create your views here.

@csrf_exempt
def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = 3600),
        'iat': datetime.datetime.utcnow()
    }, 'access_secret', algorithm='HS256')


def decode_access_token(token):
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')
        return payload['user_id']
    except:
        raise exceptions.AuthenticationFailed('unauthenticated')

@csrf_exempt
def login(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        #print(password)

        #print(encryptedPassword)

        if not User.objects.filter(email = email).exists():
            print("here")
            return JsonResponse({
                "message" : "Failed",
                "error" : "Invalid Credantial"
            })

        user = User.objects.filter(email = email)[0]
        # print(user.password)
        if not check_password(password, user.password):
            return JsonResponse({
                "message" : "Failed",
                "error" : "Invalid Credantial"
            })

        accessToekn = create_access_token(user.id)

        return JsonResponse({
            "messgae" : "success",
            "token" : accessToekn
        })
        
    return JsonResponse({"message":"This is not post request"})

@csrf_exempt
def registerVoter(request, id):
    if request.method == "POST":
        body = json.loads(request.body)

        fullName = body['fullName']
        university = body['university']
        email = body['email']
        password = body['password']
        voted = False
        isSuperAdmin = False


        if User.objects.filter(email = email).exists():
            return JsonResponse({
                "message" : "Failed",
                "error" : "user with this email id already exist"
            })

        encryptedPassword = make_password(password)


        Voter.objects.create(
            fullName = fullName,
            university = university,
            email = email,
            password = encryptedPassword,
            voted = voted,
            isSuperAdmin = isSuperAdmin
        )

        if id == 1 :
            return JsonResponse({
                "messgae" : "success"
            })

        return login(request)


   

