from django.urls import path
from . import views
from .views import UserRegistrationView, LogoutView, UserLoginView,Sure_kuleft


app_name = 'accounts'

urlpatterns = [
    path("login/", UserLoginView.as_view(), name="user_login"),
    path("out", LogoutView.as_view(), name="optout"),
    path("logout/", Sure_kuleft, name="user_logout"),
    path( "register/", UserRegistrationView.as_view(), name="user_registration"),
    #path('index', views.index, name='index'),
    path('settings', views.settings, name='settings'),
    path('upload', views.upload, name='upload'),
    #path('follow', views.follow, name='follow'),
    #path('search', views.search, name='search'),
    #path('profile/<str:pk>', views.profile, name='profile'),
    #path('like-post', views.like_post, name='like-post'),
]
