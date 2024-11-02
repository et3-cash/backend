from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from datetime import timedelta
from django.utils import timezone
import random
from django.core.validators import RegexValidator

phone_regex = r"^(?:\+20|0)?1[0125][0-9]{8}$"

class UserManager(BaseUserManager):
    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone number")
        
        

        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password=None):
        user = self.create_user(phone_number=phone_number, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone_number = models.CharField(max_length=15, unique=True, validators=[RegexValidator(regex=phone_regex, message="Enter a valid Egyptian phone number")])
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)  
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def generate_otp(self):
        self.otp_code = f"{random.randint(100000, 999999)}"
        self.save()
        return self.otp_code

    def is_valid(self):
        return not self.is_verified and self.created_at >= timezone.now() - timedelta(minutes=10)

    def __str__(self):
        return self.phone_number


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def deposit(self, amount):

        if amount < 0:
            raise ValueError("Amount must be positive")

        self.balance += amount
        self.save()

    def withdraw(self, amount):
        if amount < 0:
            raise ValueError("Amount must be positive")

        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient balance")
    
    def __str__(self):
        return self.user.phone_number


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer', 'Transfer'),
        ('payment', 'Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    transaction_type = models.CharField(choices=TRANSACTION_TYPES, max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)


class Biller(models.Model):
    name = models.CharField(max_length=255)
    biller_id = models.CharField(max_length=20, unique=True)

class BillPayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    biller = models.ForeignKey(Biller, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)
