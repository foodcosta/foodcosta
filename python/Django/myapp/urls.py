from django.urls import path
from . import views

urlpatterns = [
    path('',views.sign_in,name='sign-in'),
    path('index/',views.index,name='index'),
    path('sign-up/',views.sign_up,name='sign-up'),
    path('otp/',views.otp,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('profile/',views.profile,name='profile'),
]