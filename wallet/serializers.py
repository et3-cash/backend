import re

from rest_framework import serializers
from .models import User, Account, Transaction, Biller, BillPayment


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'date_joined', 'is_active', 'password']

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ['id', 'user', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'transaction_type', 'amount', 'created_at', 'description']


class BillerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Biller
        fields = ['id', 'name', 'biller_id']

class BillPaymentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    biller = BillerSerializer(read_only=True)

    class Meta:
        model = BillPayment
        fields = ['id', 'user', 'biller', 'amount', 'date_paid']