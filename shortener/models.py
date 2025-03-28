from django.conf import settings
from django.db import models
from django.utils import timezone


class URLMap(models.Model):
    original_url = models.URLField(max_length=settings.URL_ORIGINAL_MAX_LENGTH)
    hash = models.CharField(max_length=settings.URL_HASH_MAX_LENGTH, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(default=timezone.now() + settings.URL_EXPIRATION_DELTA)
