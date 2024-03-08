from django.urls import path

from .views import DepositMoneyView, WithdrawMoneyView, TransactionRepostView, eshopCart , MboaCoins


app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionRepostView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("mboapay/", eshopCart.as_view(), name="eshopcart"),
    path("mboaCoins/", MboaCoins.as_view(), name="eshopcart"),
]
