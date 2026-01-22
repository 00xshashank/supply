from django.urls import path

from .views import *

urlpatterns = [
    path("signup/", signupRoute, name="SignUp"),
    path("login/", loginRoute, name="LogIn"),
    path("logout/", logoutRoute, name="LogOut"),
    path("is-authenticated/", isUserAuthenticated, name="IsUserAuthenticated"),
    path("first-chat/", indexChat, name="FirstChat"),
    path("create-project/", createProject, name="CreateProject"),
    path("get-projects/", getProjects, name="GetProjects"),
    path("select-project/", selectProject, name="SelectProject"),
    path("get-chats/", getAllMessages, name="GetAllMessages"),
    path("status/", getStatus, name="GetStatus"),
    path("node-information/", nodeResearchInformation, name="NodeResearchInformation"),
    path("research/", getResearch, name="GetResearch")
    # path("csrf/", csrf, name="CSRF")
]