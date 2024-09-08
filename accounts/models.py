from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from .otp_utils import generate_otp


class OtpToken(models.Model):
    otp = models.CharField(max_length=6, default=generate_otp)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(blank=True, null=True)


class User(AbstractUser):
    first_name = models.CharField(_('first name'), blank=False, max_length=150)
    last_name = models.CharField(_('last name'), blank=False, max_length=150)
    email = models.EmailField(_('email address'), blank=False)
    is_email_verified = models.BooleanField(default=False)
    email_otp = models.ForeignKey(OtpToken, on_delete=models.SET_NULL, null=True, blank=True)
    

