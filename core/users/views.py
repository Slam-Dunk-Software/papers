from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from .models import UserCreate, UserLogin
from pydantic import ValidationError
from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect

# FIXME: Redirect when user is already logged in
# FIXME: Add password_reset logic
# FIXME: Add OAuth?
def signup_view(request: Any) -> HttpResponse:
    if request.method == "POST":
        try:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password = request.POST.get('password')

            user_data = UserCreate(username=username, email=email, password=password)

            if User.objects.filter(username=user_data.username).exists():
                return render(request, 'errors.html', {'error': "Username already exists"})
            
            if User.objects.filter(email=user_data.email).exists():
                return render(request, 'errors.html', {'error': "Email already exists"})

            user = User.objects.create_user(username=user_data.username, email=user_data.email, password=user_data.password)
            login(request, user)
            response = HttpResponse("No content.")
            response["HX-Redirect"] = "/"  # FIXME: Can I add a flash here? -- Signup successful!
            return response

        except ValidationError as e:
            return render(request, 'errors.html', {'error': e.errors()})

    return render(request, "signup.html")

# FIXME: Add password_reset logic
# FIXME: Add OAuth?
def login_view(request: Any) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate with pydantic
        user_data = UserLogin(username=username, password=password)

        user = authenticate(request, username=user_data.username, password=user_data.password)
        if user is not None:
            login(request, user)
            response = HttpResponse("No content.")
            response["HX-Redirect"] = "/"  # FIXME: Can I add a flash here?
            return response

        return render(request, 'errors.html', {'error': "Invalid credentials"})

    return render(request, "login.html")

# FIXME: Add OAuth?
def logout_view(request: Any) -> HttpResponse:
    logout(request)
    return redirect("login")
