from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from wallet.models import Account, BillPayment, Biller, Transaction
from wallet.serializers import BillPaymentSerializer, TransactionSerializer


class PayBillView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        biller_id = request.data.get('biller_id')
        amount = request.data.get('amount')

        account = Account.objects.get(user__phone_number=phone_number)
        biller = Biller.objects.get(biller_id=biller_id)

        try:
            account.withdraw(amount)
            bill_payment = BillPayment.objects.create(user=account.user, biller=biller, amount=amount)
            transaction = Transaction.objects.create(user=account.user, transaction_type='payment', amount=amount, description=f'Bill payment to {biller.name}')
            return Response({
                "bill_payment": BillPaymentSerializer(bill_payment).data,
                "transaction": TransactionSerializer(transaction).data
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RechargeMobileView(APIView):

    def post(self, request):
        phone_number = request.data.get('phone_number')
        amount = request.data.get('amount')

        account = Account.objects.get(user__phone_number=phone_number)

        try:
            account.withdraw(amount)
            transaction = Transaction.objects.create(user=account.user, transaction_type='payment', amount=amount, description='Mobile recharge')
            return Response(TransactionSerializer(transaction).data, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
