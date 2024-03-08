from django.urls import path
from .views import MboaNFTs, index, biz

urlpatterns = [
	path('index/', index, name='index'),
	path('biz', biz, name='biz'),
	path('MboaNFTs', MboaNFTs, name='MboaNFTs'),

]
