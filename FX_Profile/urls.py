from . import views
from django.urls import path
from .views import (
    ItemDetailView,
    CheckoutView,
    HomeView,
    OrderSummaryView,
    add_to_cart,
    remove_from_cart,
    remove_single_item_from_cart,
    PaymentView,
    AddCouponView,
    RequestRefundView
)

urlpatterns = [

    path('HeroPage', views.homepage, name='homepage'),
    path('', views.Ganji, name='home'),
    path('ad', views.ad, name='ad'),
    path('page', views.page, name='page'),
    path('wallet/ID', views.ID, name='ID'),
    path('wallet/banks', views.banks, name='banks'),
    path('wallet', views.hero, name='wallet'),
    path('Swap', views.Swap, name='Swap'),
    path('dev', views.dev, name='dev'),
    path('pro', views.pro, name='pro'),
    path('Deposit', views.Deposit, name='Deposit'),
    path('setting', views.setting, name='setting'),
    path('stk', views.stk, name='stk'),
    path('LipaNaMpesa', views.LipaNaMpesa, name='LipaNaMpesa'),
    path('Duka', HomeView, name='home'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('order-summary/', OrderSummaryView.as_view(), name='order-summary'),
    path('product/<slug>/', ItemDetailView.as_view(), name='product'),
    path('add-to-cart/<slug>/', add_to_cart, name='add-to-cart'),
    path('add-coupon/', AddCouponView.as_view(), name='add-coupon'),
    path('remove-from-cart/<slug>/', remove_from_cart, name='remove-from-cart'),
    path('remove-item-from-cart/<slug>/', remove_single_item_from_cart,name='remove-single-item-from-cart'),
    path('payment/<payment_option>/', PaymentView.as_view(), name='payment'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund')
]
