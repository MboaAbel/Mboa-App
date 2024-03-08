from django.urls import re_path as url, include,path
from . import views

test_patterns = [
	url(r'^$', views.index, name='django_daraja_index'),
	url(r'^oauth/success', views.oauth_success, name='test_oauth_success'),
	url(r'^stk-push/success', views.stk_push_success, name='test_stk_push_success'),
	url(r'^business-payment/success', views.business_payment_success, name='test_business_payment_success'),
	url(r'^salary-payment/success', views.salary_payment_success, name='test_salary_payment_success'),
	url(r'^promotion-payment/success', views.promotion_payment_success, name='test_promotion_payment_success'),
]

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^tests/', include(test_patterns)),
    url(r'^oauth/success', views.oauth_success, name='test_oauth_success'),
    url('Offline', views.Offline, name='offline'),
    url('Query_stk_push', views.Query_stk_push, name='Query_stk_push'),
    path('b2c', views.b2c_payment, name='b2c_payment'),
	url(r'^stk-push/success', views.stk_push_success, name='test_stk_push_success'),
	url(r'^business-payment/success', views.business_payment_success, name='test_business_payment_success'),
	url(r'^salary-payment/success', views.salary_payment_success, name='test_salary_payment_success'),
	url(r'^promotion-payment/success', views.promotion_payment_success, name='test_promotion_payment_success'),
]

