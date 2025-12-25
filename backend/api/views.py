from django.shortcuts import render
from django.http import request, HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.views.decorators.csrf import ensure_csrf_cookie

from pydantic import BaseModel, ValidationError
import json

class UserValidation(BaseModel):
    username: str
    email: str
    password: str

class LoginValidation(BaseModel):
    username: str
    password: str

@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({ "message": "CSRF cookie set" })

def signup(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        try:
            user = UserValidation(**json_body)
        except ValidationError as V:
            print(f"Error occurred during input validation:\n\n{V}")
            return JsonResponse({
                "status": "failure",
                "message": "Malformed request"
            })
        
        try:
            created_user = User.objects.create_user(
                username=user.username,
                email=user.email,
                password=user.password
            )
            created_user.save()
        except IntegrityError as I:
            print(f"Integrity Error occurred during user creation:\n\n{I}")
            return JsonResponse({
                "status": "failure",
                "message": "User with given username already exists"
            })

        print(f"Uname: {user.username} has been registered")

        return JsonResponse({
            "status": "success",
            "message": "User created successfully"
        })

    return JsonResponse({
        "status": "failure",
        "message": "Method not allowed on this route"
    })

def Login(request):
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        json_body = json.loads(body_unicode)
        print(json_body)
        login_attempt = LoginValidation(**json_body)

        user = authenticate(request=request, credentials={ 'username': login_attempt.username, 'password': login_attempt.password})
        if user is not None:
            login(request)
            return JsonResponse({
                "status": "success",
                "message": "User successfully logged in"
            })
        else:
            return JsonResponse({
                "status": "failure",
                "messsage": "No such user found, please check credentials or try signing up instead"
            })
        
    return JsonResponse({
        "status": "failure",
        "message": "Method not allowed on this route"
    })


def Logout(request):
    logout(request)
