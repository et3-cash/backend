import re

from .models import Account, Transaction, Biller, BillPayment
from django.contrib.auth import get_user_model

from rest_framework import serializers
from django.contrib.auth import get_user_model

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = get_user_model()
        fields = ['id', 'phone_number', 'date_joined', 'is_active', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')  
        user = super().create(validated_data)  
        user.set_password(password)  
        user.save()
        return user


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