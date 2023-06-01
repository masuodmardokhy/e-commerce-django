from django.urls import path
from .import views

app_name ='accounts'

urlpatterns =[             #function base view urls
    path('register/', views.user_register,name='register'),
    path('login/', views.user_login,name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.user_profile,name='profile'),
    path('update/', views.user_update,name='update'),
    path('change_password/',views.change_password,name='change_password'),

]