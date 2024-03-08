# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from accounts.models import UserBankAccount,UserAddress


msee = settings.AUTH_USER_MODEL
user = msee


class AccessToken(models.Model):
	token = models.CharField(max_length=30)
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		get_latest_by = 'created_at'

	def __str__(self):
		return self.token
	
	
class MpesaPayment(models.Model):
	MerchantRequestID = models.CharField(max_length=15)
	CheckoutRequestID = models.CharField(max_length=30)
	ResponseCode = models.CharField(max_length=30)
	ResponseDescription = models.CharField(max_length=30)
	CustomerMessage = models.CharField(max_length=30)
	paid_at = models.DateTimeField(auto_now_add=True)
	amount = models.CharField(max_length=15)
	
	class Meta:
		get_latest_by = 'paid_at'

	def __str__(self):
		return self.MerchantRequestID


class STK_Response(models.Model):
	phone_number = models.CharField(max_length=15)
	amount = models.CharField(max_length=15)
	paid_at = models.DateTimeField(auto_now_add=True)
	account_reference = models.CharField(max_length=30)
	transaction_desc = models.CharField(max_length=30)
	occassion = models.CharField(max_length=30)
	checkoutRequestID = models.CharField(max_length=30)
	timestamp = models.IntegerField()
	
	class Meta:
		get_latest_by = 'paid_at'
	
	def __str__(self):
		return self.phone_number
	