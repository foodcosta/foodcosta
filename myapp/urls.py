
from os import name
from django.urls import path
from . import views

urlpatterns = [

path('index/', views.index, name='index'),
path('', views.sign_in, name='sign-in'),
path('menu/', views.menu, name='menu'),
path('sign-up/', views.sign_up, name='sign-up'),
path('profile/', views.profile, name='profile'),
path('header/', views.header, name='header'),
path('logout/', views.logout, name='logout'),
path('otp/', views.otp, name='otp'),
path('forgot-password/', views.forgot_password, name='forgot-password'),
path('item/', views.item, name='item'),
path('sub-item/', views.sub_item, name='sub-item'),
path('Cart1/', views.Cart1, name='Cart1'),
path('viewbook/', views.viewbook, name='viewbook'),
path('cart/<int:pk>',views.cart, name='cart'),
path('Cart1/paymenthandler/<int:pk>', views.paymenthandler, name='paymenthandler'),
path('remove-item/<int:pk>', views.remove_item, name='remove-item'),



] 
