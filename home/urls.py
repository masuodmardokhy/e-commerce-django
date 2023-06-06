from django.contrib import admin
from django.urls import path
from .views import *
from . import views



app_name ='home'
urlpatterns = [
    path('home/',Home.as_view(), name='home'),     #class base view url
    path('store/', views.store, name='store'),    #function base view url
    path('logout', views.logout, name='logout'),
    path('login', Login.as_view(), name='login'),
    path('register', Register.as_view(), name='register'),
    path('check_out', CheckOut.as_view(), name='check_out'),
    path('order_view', OrderView.as_view(), name='order_view'),
    path('cart', Cart.as_view(), name='cart'),

]