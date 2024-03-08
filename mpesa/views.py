# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse, JsonResponse
from mpesa.mpesa.core import MpesaClient
from .mpesa.utils import mpesa_config
from django.shortcuts import render, get_object_or_404
from mpesa.forms import PaymentForm, QueryForm

cl = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = 'https://api.darajambili.com/b2c/result'

def index(request):
	return render(request, 'mpesa/Offline.html')


def Query_stk_push(request):
	global response
	if request.method == 'POST':
		form = QueryForm(request.POST)
		if form.is_valid():
			#phone_number = form.cleaned_data['phone_number']
			# amount = form.cleaned_data['amount']
			checkout_request_id = form.cleaned_data['CheckoutRequestID']
			data = cl.stk_status_query(checkout_request_id)
			response = data
			print(checkout_request_id)
		return JsonResponse(response ,safe=False)
	else:
		form = PaymentForm()
	return render(request, 'mpesa/Query.html', {'form': form})


def oauth_success(request):
	r = cl.access_token()
	return JsonResponse(r, safe=False)


def Ni_Push(request):
	# Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
	if request.method == 'POST':
		form = PaymentForm(request.POST)
		if form.is_valid():
			phone_number = form.cleaned_data['phone_number']
			amount = form.cleaned_data['amount']
			# amount = form.cleaned_data['amount']
			account_reference = 'MboaEx Account'
			transaction_desc = 'MboaEx Account Deposit'
			callback_url = stk_push_callback_url
			response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
			print(response)
		return HttpResponse(response)
	else:
		form = PaymentForm()
	return render(request, 'transactions/transaction_report.html', {'form': form})


def stk_push_success(request):
	phone_number = mpesa_config('LNM_PHONE_NUMBER')
	amount = 1
	# amount = form.cleaned_data['amount']
	account_reference = 'MboaEx'
	transaction_desc = 'MboaEx Account Deposit'
	callback_url = stk_push_callback_url
	r = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
	return JsonResponse(r.response_description, r, safe=False)

def business_payment_success(request):
	phone_number =mpesa_config('B2C_PHONE_NUMBER')
	amount = 1
	# amount = form.cleaned_data['amount']
	transaction_desc = 'Business Payment Description'
	occassion = 'Test business payment occassion'
	callback_url = b2c_callback_url
	r = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)

def salary_payment_success(request):
	phone_number = mpesa_config('B2C_PHONE_NUMBER')
	amount = 1
	# amount = form.cleaned_data['amount']
	transaction_desc = 'Salary Payment Description'
	occassion = 'Test salary payment occassion'
	callback_url = b2c_callback_url
	r = cl.salary_payment(phone_number, amount, transaction_desc, callback_url, occassion)
	return JsonResponse(r.response_description, safe=False)

def promotion_payment_success(request):
	# phone_number = mpesa_config('B2C_PHONE_NUMBER')
	phone_number= '0794462494'
	amount = 10
	# amount = form.cleaned_data['amount']
	transaction_desc = 'Promotion Payment Description'
	occassion = 'Test promotion payment occassion'
	callback_url = b2c_callback_url
	command_id = 'PromotionPayment'
	r = cl.promotion_payment(phone_number, amount, transaction_desc, callback_url, occassion,command_id)
	return HttpResponse(r)


def b2c_payment(request):
	if request.method == 'POST':
		form = PaymentForm(request.POST)
		if form.is_valid():
			phone_number = mpesa_config('B2C_PHONE_NUMBER')
			amount = form.cleaned_data['amount']
			# amount = form.cleaned_data['amount']
			transaction_desc = form.cleaned_data['transaction_desc']
			occassion = form.cleaned_data['occassion']
			callback_url = b2c_callback_url
			r = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)
			response = r
			print(response)
			return JsonResponse(response.response_description, safe = False)
		else:
			form = PaymentForm()
		return render(request, 'transactions/transaction_report.html', {'form': form})


def Offline(request):
    return render(request, 'mpesa/Offline.html')
 