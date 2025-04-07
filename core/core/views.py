import hmac
import hashlib
import base64
import json
from typing import Optional
from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.decorators.csrf import csrf_exempt
from .models import WebhookLog, Customer, CustomerAddress
from .validators import CustomerCreateData
from pydantic import ValidationError


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
    if not verify_shopify_webhook(request, settings.SHOPIFY_WEBHOOK_SIGNATURE):
        return HttpResponse(status=403)

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400)
    
    topic = request.headers.get("X-Shopify-Topic", "unknown")
    shop_domain = request.headers.get("X-Shopify-Shop-Domain", "unknown")

    # Log the whole payload and indicate that we received an event
    # from Shopify (useful for debugging)
    WebhookLog.objects.create(
        topic=topic,
        shop_domain=shop_domain,
        payload=data,
    )

    # Call the appropriate handler based on the topic
    if topic == "customers/create":
        return handle_customer_create(data, shop_domain)

    # Add other topics as needed, for example:
    # elif topic == "orders/create":
    #     return handle_order_create(data, shop_domain)
    
    # NOTE: We probably shouldn't reach this anymore, now that we have the
    #       individual topic handling
    return HttpResponse(status=200)

def handle_customer_create(data: dict, shop_domain: str) -> HttpResponse:
    try:
        customer_data = CustomerCreateData(**data)
    except ValidationError as e:
        # FIXME: I don't like this topic string being built this this--
        #        make it more standardized / constantized?
        WebhookLog.objects.create(
            topic="customers/create - VALIDATION ERROR",
            shop_domain=shop_domain,
            received_at=timezone.now(),
            payload={
                "error": e.errors(),
                "raw_data": data,
            },
        )
        return HttpResponse(f"Invalid data: {e}", status=400)
    
    WebhookLog.objects.create(
        topic="customers/create - DEBUG",
        shop_domain=shop_domain,
        received_at=timezone.now(),
        payload={
            "message": "Debugging customer default address",
            "raw_data": customer_data,
        },
    )

    customer = Customer.objects.create(
        shopify_id=customer_data.id,
        first_name=customer_data.first_name or "",
        last_name=customer_data.last_name or "",
        email=customer_data.email or "",
        phone=customer_data.phone,
        note=customer_data.note or "",
        state=customer_data.state or "enabled",
        currency=customer_data.currency or "USD",
        tax_exempt=customer_data.tax_exempt or False,
        verified_email=customer_data.verified_email or False,
        created_at=parse_datetime(customer_data.created_at),
        updated_at=parse_datetime(customer_data.updated_at),
    )

    address_data = customer_data.default_address

    try:
        CustomerAddress.objects.create(
            shopify_id=address_data.id,
            customer_shopify_id=customer.shopify_id,
            customer=customer,
            address1=address_data.address1,
            address2=address_data.address2 or "",
            city=address_data.city,
            province=address_data.province,
            zip=address_data.zip,
            country=address_data.country,
            phone=address_data.phone or "",
            name=address_data.name or "",
            default=address_data.default,
        )
    except Exception as e:
        WebhookLog.objects.create(
            topic="customer address create - NO DEFAULT ADDRESS",
            shop_domain=shop_domain,
            received_at=timezone.now(),
            payload={
                "message": "Customer has no default_address",
                "raw_data": customer_data,
            },
        )

    return HttpResponse(status=200)
