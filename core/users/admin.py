from django.contrib import admin
from core.models import WebhookLog

@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('topic', 'shop_domain', 'received_at')
    search_fields = ('topic', 'shop_domain')
    list_filter = ('topic', 'received_at')
