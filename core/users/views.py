import stripe
import json
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
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

stripe.api_key = settings.STRIPE_SECRET_KEY

# FIXME: Redirect when user is already logged in
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


# FIXME: Add OAuth?
def logout_view(request: Any) -> HttpResponse:
    logout(request)
    return redirect("login")


def subscribe_view(request):
    # Funnel user towards signup if they're on the subscribe page but not authenticated
    if not request.user.is_authenticated:
        return redirect("signup")
    
    if request.method == "POST":
        # Handle subscription logic here (e.g., create a Subscription object, process payment, etc.)
        return HttpResponse("Subscription started!")  # Replace with actual subscription process
    
    return render(request, "subscribe.html")  # Show the subscription page

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
    webhook_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, webhook_secret
        )
    except ValueError:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError:
        return HttpResponse(status=400)

    # Handle the event
    if event['type'] == 'checkout.session.completed':
        pass
        # session = event['data']['object']
        # Fulfill the purchase: update user subscription, send email, etc.
    # Handle other event types if needed

    return HttpResponse(status=200)

@csrf_exempt
def create_checkout_session(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        plan = data.get('plan', 'monthly')

        # Replace these with your actual Stripe Price IDs
        price_id = 'price_monthly_id' if plan == 'monthly' else 'price_yearly_id'

        try:
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price': price_id,
                        'quantity': 1,
                    },
                ],
                mode='subscription',
                success_url=request.build_absolute_uri('/success/'),
                cancel_url=request.build_absolute_uri('/cancel/'),
            )
            return JsonResponse({'id': checkout_session.id})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request'}, status=400)


@login_required
def settings_view(request: Any) -> HttpResponse:
    # TODO: Add POST handling, for updating settings

    return render(request, "settings.html")


class CustomPasswordResetView(PasswordResetView):
    """
    Custom password reset view to ensure HTML emails are sent.
    """
    def send_mail(self, subject_template_name, email_template_name,
                  context, from_email, to_email, html_email_template_name=None):
        subject = render_to_string(subject_template_name, context).strip()
        body_text = render_to_string(email_template_name, context)
        body_html = render_to_string(html_email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body_text, from_email, [to_email])
        if html_email_template_name:
            email_message.attach_alternative(body_html, "text/html")
        email_message.send()