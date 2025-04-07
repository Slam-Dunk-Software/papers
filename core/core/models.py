from django.db import models
from django.utils import timezone

# type: ignore

class WebhookLog(models.Model):
    topic = models.CharField(max_length=255) # type: ignore
    shop_domain = models.CharField(max_length=255, blank=True, null=True) # type: ignore
    received_at = models.DateTimeField(default=timezone.now) # type: ignore
    payload = models.JSONField() # type: ignore

    def __str__(self) -> str:
        return f"{self.topic} @ {self.received_at.strftime('%Y-%m-%d %H:%M:%S')}"


# Model to capture customer information, matching the Shopify webhook data shape
class Customer(models.Model):
    id = models.BigIntegerField(primary_key=True) # type: ignore
    shopify_id = models.BigIntegerField(unique=True) # type: ignore
    email = models.EmailField(unique=True) # type: ignore
    first_name = models.CharField(max_length=100) # type: ignore
    last_name = models.CharField(max_length=100) # type: ignore
    phone = models.CharField(max_length=20, null=True, blank=True) # type: ignore
    note = models.TextField(null=True, blank=True) # type: ignore
    state = models.CharField(max_length=50, choices=[
        ('disabled', 'Disabled'),
        ('enabled', 'Enabled'),
        ('other', 'Other'),
    ], default='enabled') # type: ignore
    currency = models.CharField(max_length=10) # type: ignore
    tax_exempt = models.BooleanField(default=False) # type: ignore
    verified_email = models.BooleanField(default=False) # type: ignore
    created_at = models.DateTimeField() # type: ignore
    updated_at = models.DateTimeField() # type: ignore

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


# Model to capture address information related to a Shopify customer
class CustomerAddress(models.Model):
    id = models.BigIntegerField(primary_key=True) # type: ignore
    shopify_id = models.BigIntegerField(unique=True) # type: ignore
    customer = models.ForeignKey(Customer, related_name="addresses", on_delete=models.CASCADE) # type: ignore
    address1 = models.CharField(max_length=255) # type: ignore
    address2 = models.CharField(max_length=255, null=True, blank=True) # type: ignore
    city = models.CharField(max_length=100) # type: ignore
    province = models.CharField(max_length=100) # type: ignore
    zip = models.CharField(max_length=20) # type: ignore
    country = models.CharField(max_length=100) # type: ignore
    phone = models.CharField(max_length=20) # type: ignore
    name = models.CharField(max_length=200) # type: ignore
    default = models.BooleanField(default=False) # type: ignore
    
    def __str__(self) -> str:
        return f"{self.name}, {self.city}, {self.province}, {self.country}"
    

