from django.db import models
from django.utils import timezone

class WebhookLog(models.Model):
    topic = models.CharField(max_length=255)
    shop_domain = models.CharField(max_length=255, blank=True, null=True)
    received_at = models.DateTimeField(default=timezone.now)
    payload = models.JSONField()

    def __str__(self):
        return f"{self.topic} @ {self.received_at.strftime('%Y-%m-%d %H:%M:%S')}"
