"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import (
  home,
  shopify_customer_create_webhook,shopify_customer_update_webhook, shopify_order_create_webhook,
  shopify_fulfillment_create_webhook, shopify_fulfillment_update_webhook
)
from users.views import subscribe_view

urlpatterns = [
    path("", home, name="home"),  # Landing page
    path('admin/', admin.site.urls),
    path("users/", include("users.urls")),
    path('subscribe/', subscribe_view, name="subscribe"),
    # Shopify
    path('webhooks/customers/create', shopify_customer_create_webhook, name='shopify_customer_create_webhook'),
    path('webhooks/customers/update', shopify_customer_update_webhook, name='shopify_customer_update_webhook'),
    path('webhooks/orders/create', shopify_order_create_webhook, name='shopify_order_create_webhook'),
    path('webhooks/fulfillment/create', shopify_fulfillment_create_webhook, name='shopify_fulfillment_create_webhook'),
    path('webhooks/fulfillment/update', shopify_fulfillment_update_webhook, name='shopify_fulfillment_update_webhook'),
]
