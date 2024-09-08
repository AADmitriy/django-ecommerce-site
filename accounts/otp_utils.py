import pyotp
from datetime import datetime, timedelta
from django.utils import timezone

def generate_otp():
    totp = pyotp.TOTP(pyotp.random_base32(), interval=300)  # 5 minutes validity
    return totp.now()

def verify_otp(otp_model, input_otp):
    if otp_model.expires_at > timezone.now() and otp_model.otp == input_otp:
        return True
    
    return False
