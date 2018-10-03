from django.db import models
from django.utils import timezone

# Create your models here.
class Administrator(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=120)
    phone = models.CharField(max_length=12, blank=True, null=True)
    verification_key = models.CharField(max_length=100, default="", blank=True, null=True)
    active = models.BooleanField(default=False)
    created_at = models.DateTimeField('date created', default=timezone.now)