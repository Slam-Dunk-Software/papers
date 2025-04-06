from django.db import models
from django.utils import timezone

class WebhookLog(models.Model):
    topic = models.CharField(max_length=255)  # type: ignore
    shop_domain = models.CharField(max_length=255, blank=True, null=True)  # type: ignore
    received_at = models.DateTimeField(default=timezone.now)  # type: ignore
    payload = models.JSONField()  # type: ignore

    def __str__(self) -> str:
        return f"{self.topic} @ {self.received_at.strftime('%Y-%m-%d %H:%M:%S')}"
