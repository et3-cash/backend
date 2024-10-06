from django.contrib import admin
from .models import User, Account, OTP, Transaction, Biller, BillPayment

admin.site.register(User)
admin.site.register(Account)
admin.site.register(OTP)
admin.site.register(Transaction)
admin.site.register(Biller)
admin.site.register(BillPayment)
