# type: ignore
from django.db import models
from django.utils import timezone

class WebhookLog(models.Model):
    topic = models.CharField(max_length=255)
    shop_domain = models.CharField(max_length=255, blank=True, null=True)
    received_at = models.DateTimeField(default=timezone.now)
    payload = models.JSONField()

    def __str__(self) -> str:
        return f"{self.topic} @ {self.received_at.strftime('%Y-%m-%d %H:%M:%S')}"


# Model to capture customer information, matching the Shopify webhook data shape
# class Customer(models.Model):
#     id = models.BigIntegerField(unique=True)  # Shopify's unique customer ID
#     email = models.EmailField(unique=True)  # Customer email
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     note = models.TextField(null=True, blank=True)
#     state = models.CharField(max_length=50, choices=[
#         ('disabled', 'Disabled'),
#         ('enabled', 'Enabled'),
#         ('other', 'Other'),
#     ], default='enabled')
#     currency = models.CharField(max_length=10)
#     tax_exempt = models.BooleanField(default=False)
#     verified_email = models.BooleanField(default=False)
#     created_at = models.DateTimeField()
#     updated_at = models.DateTimeField()

#     def __str__(self) -> str:
#         return f"{self.first_name} {self.last_name}"
    


# # Model to capture address information related to a Shopify customer
# class CustomerAddress(models.Model):
#     id = models.BigIntegerField(unique=True)  # Shopify's unique address ID
#     customer = models.ForeignKey(Customer, related_name="addresses", on_delete=models.CASCADE)
#     address1 = models.CharField(max_length=255)
#     address2 = models.CharField(max_length=255, null=True, blank=True)
#     city = models.CharField(max_length=100)
#     province = models.CharField(max_length=100)
#     zip = models.CharField(max_length=20)
#     country = models.CharField(max_length=100)
#     phone = models.CharField(max_length=20)
#     name = models.CharField(max_length=200)
#     default = models.BooleanField(default=False)
    
#     def __str__(self) -> str:
#         return f"{self.name}, {self.city}, {self.province}, {self.country}"