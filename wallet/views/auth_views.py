from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import AllowAny, IsAuthenticated

from wallet.models import User, OTP, Account
from wallet.serializers import UserSerializer
from wallet.services.auth_service import create_user, authenticate_user, send_otp, verify_otp

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Generate and save OTP
            otp = send_otp(user.phone_number)

            return Response({
                "user": UserSerializer(user).data,
                "otp": otp  # Include the OTP in the response
            }, status=status.HTTP_201_CREATED)
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
        
        if not self.user.is_active:
            raise serializers.ValidationError(
                {"error": "User account is not active."}
            )
        
        return data

class LoginUserView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


