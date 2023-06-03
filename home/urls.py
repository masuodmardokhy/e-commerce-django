from django.contrib import admin
from django.urls import path
from .views import *
from . import views


app_name ='home'
urlpatterns = [
    path('',home.as_view(), name='home'),     #class base view url
    path('store/', views.store, name='store'),    #function base view url

]