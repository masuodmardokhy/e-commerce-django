from django.urls import path
from .import views

app_name ='accounts'

urlpatterns =[             #function base view urls
    path('', views.accounts_home, name='accounts_home'),
    path('home_login/', views.accounts_home_login, name='accounts_home_login'),
    path('register/', views.user_register,name='register'),
    path('login/', views.user_login,name='login'),
    path('home/', views.accounts_home, name='accounts_home'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile,name='profile'),
    path('update/', views.user_update,name='update'),
    path('change_password/',views.change_password,name='change_password'),

]