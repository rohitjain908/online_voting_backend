from django.shortcuts import render, HttpResponse
import jwt, datetime
from rest_framework import exceptions
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User

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
        #print(request.method)
        body = json.loads(request.body)
        #print(body)
        email = body['email']
        password = body['password']

        if not User.objects.filter(email = email, password = password).exists():
            return JsonResponse({
                "message" : "Invalid Credantial"
            })

        user = User.objects.filter(email = email, password = password)[0]
        accessToekn = create_access_token(user.id)

        return JsonResponse({
            "messgae" : "success",
            "token" : accessToekn
        })
        
    return JsonResponse({"message":"This is not post request"})
   

