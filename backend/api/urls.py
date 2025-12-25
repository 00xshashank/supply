from django.urls import path

from .views import signup, Login, csrf, Logout

urlpatterns = [
    path("signup/", signup, name="SignUp"),
    path("login/", Login, name="LogIn"),
    path("logout/", Logout, name="LogOut"),
    path("csrf/", csrf, name="CSRF")
]