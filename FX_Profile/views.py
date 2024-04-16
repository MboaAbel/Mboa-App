from mpesa.forms import PaymentForm

import stripe
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django import template
import json
from accounts.models import UserAddress
from .forms import  PaymentForm
from django.http import HttpResponse
from mpesa.mpesa.core import MpesaClient
from mpesa.mpesa.utils import mpesa_config
from django.shortcuts import render




stripe.api_key = settings.STRIPE_SECRET_KEY
register = template.Library()


cl = MpesaClient()
stk_push_callback_url = 'https://api.darajambili.com/express-payment'
b2c_callback_url = 'https://api.darajambili.com/b2c/result'


def parse_stk_result(self, result):
	"""
	Parse the result of Lipa na MPESA Online Payment (STK Push)

	Returns:
		The result data as an array
	"""
	
	payload = json.loads(result)
	data = {}
	callback = payload['Body']['stkCallback']
	data['ResultCode'] = callback['ResultCode']
	data['ResultDesc'] = callback['ResultDesc']
	data['MerchantRequestID'] = callback['MerchantRequestID']
	data['CheckoutRequestID'] = callback['CheckoutRequestID']
	data['ResponseCode'] = callback['ResponseCode']
	data['ResponseDescription'] = callback['ResponseDescription']
	data['ResultCode'] = callback['ResultCode']
	data['ResultDesc'] = callback['ResultDesc']
	
	metadata = callback.get('CallbackMetadata')
	if metadata:
		metadata_items = metadata.get('Item')
		for item in metadata_items:
			data[item['Name']] = item.get('Value')
	
	return data


def stk_Push(request):
	# Use a Safaricom phone number that you have access to, for you to be able to view the prompt.
	global context
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
			data = response
			print(data)
			context = {'data': data}
		#return HttpResponse(response)
		return render(request, 'mpesa/STK-Response.html')
	else:
		form = PaymentForm()
	return render(request, 'transactions/transaction_report.html', {'form': form})




def b2c_payment(request):
	if request.method == 'POST':
		form = PaymentForm(request.POST)
		if form.is_valid():
			phone_number = mpesa_config('B2C_PHONE_NUMBER')
			amount = form.cleaned_data['amount']
			transaction_desc = form.cleaned_data['transaction_desc']
			occassion = form.cleaned_data['occassion']
			callback_url = b2c_callback_url
			r = cl.business_payment(phone_number, amount, transaction_desc, callback_url, occassion)
			response = r
			print(response)
			return HttpResponse(response)
		else:
			form = PaymentForm()
		return render(request, 'transactions/transaction_report.html', {'form': form})
		

@login_required(login_url='/accounts/login')
def hero(request):
	if request.user.is_anonymous:
		return redirect('user_login.html')
	return render(request, 'fx/wallet.html')

@login_required(login_url='/accounts/login')
def stk_push_callback(request):
	data = request.body
	return HttpResponse(data)


@login_required(login_url='/accounts/login')
def dev(request):
	if request.user.is_anonymous:
		return redirect('user_login.html')
	return render(request, 'fx/cv.html')


@login_required(login_url='/accounts/login')
def SettingView(request):
	if request.user.is_anonymous:
		return redirect('user_login.html')
	return render(request, 'fx/setting.html')
	

@login_required(login_url='/accounts/login')
def banks(request):
	return render(request, 'fx/Banks.html')


def MboaEX(request):
	return render(request, 'fx/ad.html')


@login_required(login_url='/accounts/login')
def LipaNaMpesa(request):
	return render(request, 'mpesa/LipaNaMpesa.html')


@login_required(login_url='/accounts/login')
def ID(request):
	return render(request, 'fx/Mboa-Id.html')

@login_required(login_url ='/accounts/login')
def page(request):
	return render(request, 'fx/page.html')


def Deposit(request):
	return render(request, 'fx/Deposit.html')


def BrokerView(request):
	#  blog= miner.Blockchain_miner()
	return render(request, 'Broker/product.html')


@login_required(login_url='/accounts/login')
def setting(request):
	return render(request, 'fx/setting.html')


@login_required(login_url='/accounts/login')
def Swap(request):
	return render(request, 'fx/Swap.html')


def ex_setting(request):
	user_profile = UserAddress.objects.get(user=request.user)
	
	if request.method == 'POST':
		
		if request.FILES.get('image') == None:
			image = user_profile.profileimg
			bio = request.POST['bio']
			apartment_address = request.POST['apartment_address']
			location = request.POST['location']
			# slug = request.POST['slug']
			postal_code = request.POST['postal_code']
			
			user_profile.profileimg = image
			# user_profile.slug = slug
			user_profile.bio = bio
			user_profile.postal_code = postal_code
			user_profile.location = location
			user_profile.apartment_address = apartment_address
			user_profile.save()
		if request.FILES.get('image') != None:
			image = request.FILES.get('image')
			bio = request.POST['bio']
			postal_code = request.POST['postal_code']
			location = request.POST['location']
			apartment_address = request.POST['apartment_address']
			# slug = request.POST['slug']
			
			user_profile.profileimg = image
			user_profile.postal_code = postal_code
			user_profile.bio = bio
			user_profile.location = location
			user_profile.apartment_address = apartment_address
			# user_profile.slug = slug
			user_profile.save()
		return render(request, 'fx/setting.html')
	return render(request, 'fx/ex_setting.html', {'user_profile': user_profile})


@login_required(login_url='/accounts/login')
def Member(request):
	if request.user.is_anonymous:
		return redirect('user_login.html')
	return render(request, 'core/users.html')

