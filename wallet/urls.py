from django.urls import path
from .views.auth_views import RegisterUserView, LoginUserView, VerifyOTPView

from .views.account_views import CheckBalanceView, DepositMoneyView, WithdrawMoneyView, ChangePasswordView
from .views.transaction_views import TransferMoneyView
from .views.payment_views import PayBillView, RechargeMobileView
from .views.transaction_history_views import TransactionHistoryView, TransactionDetailView

from rest_framework_simplejwt.views import TokenRefreshView


urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('login/', LoginUserView.as_view(), name='login_user'),
    path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('balance/', CheckBalanceView.as_view(), name='check_balance'),
    path('deposit/', DepositMoneyView.as_view(), name='deposit_money'),
    path('withdraw/', WithdrawMoneyView.as_view(), name='withdraw_money'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('transfer/', TransferMoneyView.as_view(), name='transfer_money'),
    path('pay-bill/', PayBillView.as_view(), name='pay_bill'),
    path('recharge-mobile/', RechargeMobileView.as_view(), name='recharge_mobile'),
    path('transaction-history/', TransactionHistoryView.as_view(), name='transaction_history'),
    path('transaction/<int:transaction_id>', TransactionDetailView.as_view(), name='generate_statement'),
]
