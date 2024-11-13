from django.db import models
import uuid
from django.conf import settings

# Create your models here.
class Email(models.Model):
    email=models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    timestamp=models.DateTimeField(auto_now_add=True)

class EmailVerificationEvent(models.Model):
    email = models.EmailField()
    parent = models.ForeignKey(Email, on_delete=models.SET_NULL, null=True)
    expired = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    token = models.UUIDField(default=uuid.uuid1)
    last_attempt_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    expired_at = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True
    )
    timestamp=models.DateTimeField(auto_now_add=True)

    def get_link(self):
        return f"{settings.BASE_URL}/verify/{self.token}"
    
