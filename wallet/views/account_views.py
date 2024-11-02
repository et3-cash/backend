from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from wallet.models import Account, Transaction
from wallet.serializers import AccountSerializer, TransactionSerializer, UserSerializer

from wallet.permissions import IsOwner

class CheckBalanceView(APIView):
     
    permission_classes = [IsAuthenticated, IsOwner]
    def get(self, request):
        try:
            # Use request.user to get the user's phone number from the JWT
            account = Account.objects.get(user=request.user)
            serializer = AccountSerializer(account)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Account.DoesNotExist:
            return Response({"message": "Account not found"}, status=status.HTTP_404_NOT_FOUND)

class DepositMoneyView(APIView):
     
    permission_classes = [IsAuthenticated, IsOwner]


    def post(self, request):

        amount = request.data.get('amount')

        if amount and amount < 0:
            return Response({"message": "Amount must be positive"}, status=status.HTTP_400_BAD_REQUEST)

        account = Account.objects.get(user=request.user)
        account.deposit(amount)
        transaction = Transaction.objects.create(
            user=account.user, 
            transaction_type='deposit', 
            amount=amount, 
            description='Money deposited'
        )
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)

class WithdrawMoneyView(APIView):
     
    permission_classes = [IsAuthenticated, IsOwner]


    def post(self, request):
        amount = request.data.get('amount')
    
        if amount and amount < 0:
            return Response({"message": "Amount must be positive"}, status=status.HTTP_400_BAD_REQUEST)

        account = Account.objects.get(user=request.user)
        try:
            account.withdraw(amount)
            transaction = Transaction.objects.create(
                user=account.user, 
                transaction_type='withdrawal', 
                amount=amount,
                description='Money withdrawn'
            )
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(APIView):
     
    permission_classes = [IsAuthenticated, IsOwner]

    def post(self, request):
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        # We can directly access the user from the request
        user = request.user
        
        # Check if the old password is correct
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response({"message": "Incorrect old password"}, status=status.HTTP_400_BAD_REQUEST)
