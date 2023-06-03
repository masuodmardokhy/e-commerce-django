from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import *
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required



def accounts_home(request):
    return render(request,'accounts/accounts_home.html')

def accounts_home_login(request):
    return render(request,'accounts/accounts_home_login.html')


def user_register(request):
    if request.method == 'POST':
        form = UserRegisterFrom(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            User.objects.create_user(username=data['user_name'],first_name=data['first_name'],
                                     email=data['email'],last_name=data['last_name'],
                                     password=data['password_2'])
            messages.success(request, 'Your account has been successfully created. Please login', 'primary')
            return redirect('accounts:accounts_home')

    else:
        form = UserRegisterFrom()
    return render(request,'accounts/register.html',{'form':form})


def user_login(request):
    if request.method == 'POST':
        user = UserLoginForm(request.POST)
        if user.is_valid():
            data = user.cleaned_data
            try:
                user1 = authenticate(request,username=data['user'],password=data['password'])
            except:
                user1 = authenticate(request,username= User.objects.get(email=data['user']),password=data['password'])
            if user1 is not None:
                login(request, user1)
                messages.success(request,'login success','primary')
                return redirect("accounts:accounts_home_login")
            else:
                messages.error(request,'pass or user is incorrect','danger')

    else:
        user = UserLoginForm()
    return render(request,'accounts/login.html',{'user':user})


def user_logout(request):
    logout(request)
    messages.success(request,'logout success','success')
    return redirect("accounts:accounts_home")



@login_required(login_url='accounts:login')
def user_profile(request):
    profile = Profile.objects.get(user_id=request.user.id)
    return render(request,'accounts/profile.html',{'profile':profile})



@login_required(login_url='accounts:login')
def user_update(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form and profile_form .is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,'update succssfully','success')
            return redirect('accounts:profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request,'accounts/update.html',{'user_form':user_form, 'profile_form':profile_form})


@login_required(login_url='accounts:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request,form.user)
            messages.success(request,'change successfully','success')
            return redirect('accounts:profile')
        else:
            messages.error(request,'try again please','error')
            return redirect('accounts:changepass')
    else:
        form = PasswordChangeForm(request.user)
    return render(request,'accounts/changepass.html',{'form':form})