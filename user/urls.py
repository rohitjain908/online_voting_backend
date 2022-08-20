from django.urls import path
from .views import login, create_access_token


urlpatterns = [
    path("login", login, name = "login"),
    path("getToken", create_access_token, name = "token")
   
]