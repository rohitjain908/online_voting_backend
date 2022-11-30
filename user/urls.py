from django.urls import path
from .views import *


urlpatterns = [
    path("login", login, name = "login"),
    path("getToken", create_access_token, name = "token"),
    path('registerVoter', registerVoter, name = "registerVoter"),
    path('validateToken', validateToken, name = "validateToken")
]