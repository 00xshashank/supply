from django.urls import path

from .views import *

urlpatterns = [
    path("signup/", signupRoute, name="SignUp"),
    path("login/", loginRoute, name="LogIn"),
    path("logout/", logoutRoute, name="LogOut"),
    path("first-chat/", indexChat, name="FirstChat")
    # path("csrf/", csrf, name="CSRF")
]