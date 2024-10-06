from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from rest_framework.permissions import IsAuthenticated
from wallet.permissions import IsOwner

from rest_framework.generics import ListAPIView, RetrieveAPIView

from wallet.models import Transaction
from wallet.serializers import TransactionSerializer

from rest_framework_simplejwt.authentication import JWTAuthentication


class TransactionHistoryView(ListAPIView):
     
    permission_classes = [IsAuthenticated, IsOwner]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-created_at')
        


class TransactionDetailView(RetrieveAPIView):
     
    permission_classes = [IsAuthenticated, IsOwner]

    def get(self, request, transaction_id):
        try:
            transaction = Transaction.objects.get(id=transaction_id, user=request.user)
            serializer = TransactionSerializer(transaction)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Transaction.DoesNotExist:
            return Response({"message": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)