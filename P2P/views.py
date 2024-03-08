from django.shortcuts import render
import segno
from segno import helpers

# Create your views here.


def P2P_receive(request):
    qr = helpers.make_wifi(ssid='Mboa Technology', password='12834048%Mboa', security='WPA2 PSK')
    qr.save('Mboa-wifi.png', dark='green', light='white')
    
    return render(request, 'P2P/receive.html', {'qr': qr})


def P2P_send(request):
    return render(request, 'P2P/send.html')

def P2P(request):
    return render(request, 'P2P/home.html')
