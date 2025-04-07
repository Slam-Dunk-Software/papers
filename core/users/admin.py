from django.contrib import admin
from core.models import Customer, CustomerAddress, WebhookLog

@admin.register(WebhookLog)
class WebhookLogAdmin(admin.ModelAdmin):
    list_display = ('topic', 'shop_domain', 'received_at')
    search_fields = ('topic', 'shop_domain')
    list_filter = ('topic', 'received_at')
    readonly_fields = ('topic', 'shop_domain', 'received_at', 'payload')


class CustomerAddressInline(admin.StackedInline):
    model = CustomerAddress
    extra = 0
    readonly_fields = ('shopify_id',)  # optional
    can_delete = False  # optional

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('id', 'shopify_id', 'first_name', 'last_name', 'email', 'state', 'created_at')
    search_fields = ('email', 'first_name', 'last_name')
    list_filter = ('state', 'currency', 'tax_exempt')
    readonly_fields = ('created_at', 'updated_at', 'shopify_id')
    inlines = [CustomerAddressInline]

