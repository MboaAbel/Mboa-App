from django.urls import include, path
from .views import crypto

urlpatterns = [

     
     path('', crypto, name='crypto'),
    
]