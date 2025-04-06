import hmac
import hashlib
import base64
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import WebhookLog

def home(request):
    return render(request, "home.html")

@csrf_exempt
def shopify_webhook(request):
    shopify_secret = settings.SHOPIFY_WEBHOOK_SECRET
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')

    calculated_hmac = base64.b64encode(
        hmac.new(shopify_secret.encode(), request.body, hashlib.sha256).digest()
    ).decode()

    if hmac.compare_digest(calculated_hmac, hmac_header):
        data = json.loads(request.body)
        topic = request.headers.get("X-Shopify-Topic", "unknown")
        shop_domain = request.headers.get("X-Shopify-Shop-Domain", "unknown")

        WebhookLog.objects.create(
            topic=topic,
            shop_domain=shop_domain,
            payload=data
        )

        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
