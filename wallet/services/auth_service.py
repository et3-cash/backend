from django.contrib.auth import authenticate
from wallet.models import User, Account, OTP

def authenticate_user(phone_number, password):
    # This will now use the custom backend defined above
    return authenticate(phone_number=phone_number, password=password)

def create_user(phone_number, password):
    user = User.objects.create_user(phone_number=phone_number, password=password)
    Account.objects.create(user=user)
    return user

def send_otp(phone_number):
    otp_instance = OTP.objects.create(phone_number=phone_number)
    otp_code = otp_instance.generate_otp()
    
    # FUTURE WORK: Implement the logic to send the OTP via SMS or other methods here
    return otp_code

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
