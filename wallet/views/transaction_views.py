from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from wallet.models import Account, Transaction
from wallet.serializers import TransactionSerializer

class TransferMoneyView(APIView):
     
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_phone_number = request.data.get('receiver_phone_number')
        amount = request.data.get('amount')

        if amount and amount < 0:
            return Response({"message": "Amount must be positive"}, status=status.HTTP_400_BAD_REQUEST)


        sender_user = request.user  

        try:
            sender_account = Account.objects.get(user=sender_user)
            receiver_account = Account.objects.get(user__phone_number=receiver_phone_number)

            # Perform the transfer
            sender_account.withdraw(amount)
            receiver_account.deposit(amount)

            # Record the transactions
            sender_transaction = Transaction.objects.create(
                user=sender_account.user, 
                transaction_type='transfer', 
                amount=amount, 
                description=f'Transfer to {receiver_phone_number}'
            )
            receiver_transaction = Transaction.objects.create(
                user=receiver_account.user, 
                transaction_type='transfer', 
                amount=amount, 
                description=f'Transfer from {sender_user.phone_number}'
            )

            return Response({
                "sender_transaction": TransactionSerializer(sender_transaction).data,
                "receiver_transaction": TransactionSerializer(receiver_transaction).data
            }, status=status.HTTP_200_OK)
        
        except Account.DoesNotExist:
            return Response({"message": "One of the accounts does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
