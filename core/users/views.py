import json
import hmac
import hashlib
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import UserCreate, UserLogin
from pydantic import ValidationError
from typing import Any
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# FIXME: Redirect when user is already logged in
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

            messages.success(request, "Signup successful! Let's set up your subscription.")
            response = HttpResponse("No content.")
            response["HX-Redirect"] = "/subscribe"  # NOTE: This is special HTMX syntax
            return response

        except ValidationError as e:
            return render(request, 'errors.html', {'error': e.errors()})

    return render(request, "auth/signup.html")

def login_view(request: Any) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate with pydantic
        user_data = UserLogin(username=username, password=password)

        user = authenticate(request, username=user_data.username, password=user_data.password)
        if user is not None:
            login(request, user)
            next_url = request.POST.get("next", "/")  # Default to home if next isn't set
            
            response = HttpResponse("No content.")
            response["HX-Redirect"] = next_url  # Redirect correctly with HTMX
            return response

        return render(request, 'errors.html', {'error': "Invalid credentials"})

    return render(request, "auth/login.html", {"next": request.GET.get("next", "/")})


def logout_view(request: Any) -> HttpResponse:
    logout(request)
    return redirect("login")


def subscribe_view(request):
    # Funnel user towards signup if they're on the subscribe page but not authenticated
    if not request.user.is_authenticated:
        return redirect("signup")
    
    # NOTE:... this might be it. Just let people go to shopify with the buy button!
    
    return render(request, "subscribe.html")  # Show the subscription page



# TODO: Implement!
@login_required
def settings_view(request: Any) -> HttpResponse:
    # TODO: Add POST handling, for updating settings

    return render(request, "settings.html")

# FIXME: Finish hooking this up!
@csrf_exempt
def shopify_webhook(request):
    # Verify the HMAC signature
    secret = 'your_shopify_secret'
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')
    body = request.body
    computed_hmac = hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()

    if not hmac.compare_digest(hmac_header, computed_hmac):
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    # Parse the webhook data (assuming it's JSON)
    data = json.loads(body)

    # Process the data (e.g., update the user's subscription status)
    user_id = data.get('user_id')  # Example, adjust based on your data
    subscription_status = data.get('subscription_status')

    # Example: Update subscription in your database
    user = User.objects.get(id=user_id)
    user.subscription_status = subscription_status
    user.save()

    return JsonResponse({'success': True})