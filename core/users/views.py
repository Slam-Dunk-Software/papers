from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import UserCreate, UserLogin
from pydantic import ValidationError
from typing import Any
from django.http import JsonResponse
from django.shortcuts import render, redirect
import json

def signup_view(request: Any) -> JsonResponse:
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_data = UserCreate(**data)

            if User.objects.filter(username=user_data.username).exists():
                return JsonResponse({"error": "Username already exists"}, status=400)

            user = User.objects.create_user(username=user_data.username, password=user_data.password)
            login(request, user)
            return JsonResponse({"message": "Signup successful!"})

        except ValidationError as e:
            return JsonResponse({"error": e.errors()}, status=400)

    return render(request, "users/signup.html")


def login_view(request: Any) -> JsonResponse:
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            login_data = UserLogin(**data)

            user = authenticate(request, username=login_data.username, password=login_data.password)
            if user is not None:
                login(request, user)
                return JsonResponse({"message": "Login successful!"})
            return JsonResponse({"error": "Invalid credentials"}, status=400)

        except ValidationError as e:
            return JsonResponse({"error": e.errors()}, status=400)

    return render(request, "users/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")
