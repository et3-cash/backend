from django.contrib.auth import authenticate
from wallet.models import User, Account, OTP
from twilio.rest import Client
from django.conf import settings

def send_otp(phone_number):
    otp_instance = OTP.objects.create(phone_number=phone_number)
    otp_code = otp_instance.generate_otp()
    
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    
    # if the phone number does not start with '+2', add it
    if phone_number and not phone_number.startswith('+2'):
        phone_number = f'+2{phone_number}'
    
    message = client.api.account.messages.create(
        body=f"Your OTP code is {otp_code}",
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone_number
    )

    # check if the message was sent successfully
    if message.sid:
        return otp_code
    else:
        return None

def verify_otp(phone_number, otp):
    try:
        otp_instance = OTP.objects.get(phone_number=phone_number, otp_code=otp)
        if otp_instance.is_valid():
            otp_instance.is_verified = True
            otp_instance.save()
            user = User.objects.get(phone_number=phone_number)
            user.is_active = True
            user.save()
            return True
        else:
            return False
    except OTP.DoesNotExist:
        return False
