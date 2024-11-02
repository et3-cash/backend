from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated

from wallet.models import User, OTP, Account
from wallet.serializers import UserSerializer
from wallet.services.auth_service import  send_otp, verify_otp

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from wallet.serializers import AccountSerializer
from wallet.models import Account


class RegisterUserView(APIView):
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            
            try:
                # Generate and save OTP
                otp = send_otp(user.phone_number)
                # user.save()
                return Response({
                "user": UserSerializer(user).data,
                "message": "The OTP has been sent to your phone number."
            }, status=status.HTTP_201_CREATED)
            except:
                return Response({"message": "An error occurred while sending the OTP"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyOTPView(APIView):
    def post(self, request):
        phone_number = request.data.get('phone_number')
        otp = request.data.get('otp')
        if verify_otp(phone_number, otp):
            try:
                user = User.objects.get(phone_number=phone_number)
                user.is_active = True
                user.save()

                # Check if the account already exists, if not, create it
                account, created = Account.objects.get_or_create(user=user)
                
                if created:
                    message = "Account successfully activated and account created."
                else:
                    message = "Account successfully activated."

                return Response({"message": message}, status=status.HTTP_200_OK)
            
            except User.DoesNotExist:
                return Response({"message": "User does not exist."}, status=status.HTTP_404_NOT_FOUND)
        
        return Response({"message": "Invalid OTP or expired."}, status=status.HTTP_400_BAD_REQUEST)



        

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        
        data = super().validate(attrs)
        
        
        # Ensure the user is active
        if not self.user.is_active:
            raise serializers.ValidationError(
                {"error": "User account is not active."}
            )
        
        # Add user account data to the response
        try:
            account = Account.objects.get(user=self.user)
            account_data = AccountSerializer(account).data
            data['account'] = account_data
        except Account.DoesNotExist:
            data['account'] = None

        return data

class LoginUserView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


