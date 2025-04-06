import hmac
import hashlib
import base64
import json
from typing import Optional
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import WebhookLog


def home(request):
    return render(request, "home.html")

# Shopify webhooks
@csrf_exempt
def shopify_customer_create_webhook(request: HttpRequest) -> HttpResponse:
    return handle_shopify_webhook(request)

@csrf_exempt
def shopify_customer_update_webhook(request: HttpRequest) -> HttpResponse:
    return handle_shopify_webhook(request)

@csrf_exempt
def shopify_order_create_webhook(request: HttpRequest) -> HttpResponse:
    return handle_shopify_webhook(request)

@csrf_exempt
def shopify_fulfillment_create_webhook(request: HttpRequest) -> HttpResponse:
    return handle_shopify_webhook(request)

@csrf_exempt
def shopify_fulfillment_update_webhook(request: HttpRequest) -> HttpResponse:
    return handle_shopify_webhook(request)


def verify_shopify_webhook(request: HttpRequest, secret: str) -> bool:
    hmac_header: Optional[str] = request.headers.get("X-Shopify-Hmac-Sha256")
    if not hmac_header:
        return False

    calculated_hmac = base64.b64encode(
        hmac.new(secret.encode(), request.body, hashlib.sha256).digest()
    ).decode()

    return hmac.compare_digest(calculated_hmac, hmac_header)


def handle_shopify_webhook(request: HttpRequest) -> HttpResponse:
    if not verify_shopify_webhook(request, settings.SHOPIFY_WEBHOOK_SECRET):
        return HttpResponse(status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)

    topic = request.headers.get("X-Shopify-Topic", "unknown")
    shop_domain = request.headers.get("X-Shopify-Shop-Domain", "unknown")

    WebhookLog.objects.create(
        topic=topic,
        shop_domain=shop_domain,
        payload=data,
    )

    return HttpResponse(status=200)
