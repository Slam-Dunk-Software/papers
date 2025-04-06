from django.shortcuts import render
import hmac
import hashlib
import base64
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json


def home(request):
    return render(request, "home.html")


@csrf_exempt
def shopify_webhook(request) -> HttpResponse:
    # Verify the request came from Shopify
    shopify_signature = settings.SHOPIFY_WEBHOOK_SIGNATURE
    hmac_header = request.headers.get('X-Shopify-Hmac-Sha256')

    calculated_hmac = base64.b64encode(
        hmac.new(shopify_signature.encode(),request.body, hashlib.sha256).digest()
    ).decode()

    if hmac.compare_digest(calculated_hmac, hmac_header):
        data = json.loads(request.body)
        # FIXME: Do something with the Shopify data
        print("Webhook data:", data)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=403)
