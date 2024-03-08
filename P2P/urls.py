from django.urls import include, path
from .views import P2P,P2P_send,P2P_receive

urlpatterns = [

     
     path('', P2P, name='Duka'),
     path('send', P2P_send, name='send'),
     path('receive', P2P_receive, name='send')
]