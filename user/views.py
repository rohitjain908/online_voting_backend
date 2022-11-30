from django.shortcuts import render, HttpResponse
import jwt, datetime
from rest_framework import exceptions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User, Admin
from voting.models import *
from django.contrib.auth.hashers import make_password,  check_password

# Create your views here.

@csrf_exempt
def create_access_token(id):
    return jwt.encode({
        'user_id': id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds = 60),
        'iat': datetime.datetime.utcnow()
    }, 'access_secret', algorithm='HS256')

@csrf_exempt
def validateToken(request):
    body = json.loads(request.body)
    token = body['token']
    try:
        payload = jwt.decode(token, 'access_secret', algorithms='HS256')

        return JsonResponse({
            "message" : True
        })
    except:
        return JsonResponse({
            "message" : False
        })


@csrf_exempt
def login(request):
    if request.method == "POST":
        body = json.loads(request.body)
        email = body['email']
        password = body['password']
        #print(password)

        #print(encryptedPassword)

        if not User.objects.filter(email = email).exists():
            #print("here")
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

        type = "voterToken"
        if user.isSuperAdmin:
            type = "superAdminToken"

        if Admin.objects.all().filter(email = email):
            type = "adminToken"

        
        accessToekn = create_access_token(user.id)

        return JsonResponse({
            "messgae" : "success",
            "token" : accessToekn,
            "userId" : user.id,
            "type" : type
        })
        
    return JsonResponse({"message":"This is not post request"})

@csrf_exempt
def registerVoter(request):
    if request.method == "POST":
        body = json.loads(request.body)

        id = body['id']
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
                "message" : "success"
            })

        return login(request)

    return JsonResponse({"message":"This is not post request"})


   
@csrf_exempt
def registerAdmin(request):
    if request.method != 'POST':
        return JsonResponse({
            "message":"This is not post request"
        })

    body = json.loads(request.body)

    fullName = body['fullName']
    university = body['university']
    email = body['email']
    password = body['password']

    if User.objects.filter(email = email).exists():
        return JsonResponse({
            "message" : "Failed",
            "error" : "user with this email id already exist"
        })

    
    encryptedPassword = make_password(password)

    Admin.objects.create(
        fullName = fullName,
        university = university,
        email = email,
        password = encryptedPassword,
        isSuperAdmin = False    
    )

    return JsonResponse({
        "message" : "success"
    })




    

