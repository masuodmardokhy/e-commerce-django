from django import forms
from django.contrib.auth.models import User
from .models import Profile


                          #creat registerform with django , Of course, we can create it with front
class UserRegisterFrom(forms.Form):
    user_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'placeholder':  ' user name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': ' email '}))
    first_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ' first name'}))
    last_name = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': ' last name'}))
    password_1 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'enter password'}))
    password_2 = forms.CharField(max_length=20, widget=forms.PasswordInput(attrs={'placeholder': 'retry password'}))

    def clean_user_name(self):        #Authentication user name
        user = self.cleaned_data['user_name']
        if User.objects.filter(username=user).exists():
            raise forms.ValidationError('user exist')
        return user

    def clean_email(self):            #Authentication email
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('email existes')
        return email

    def clean_password_2(self):     #Authentication password
        pass_1 = self.cleaned_data['password_1']
        pass_2 = self.cleaned_data['password_2']
        if pass_1 != pass_2:
            raise forms.ValidationError('pass not match')
        elif len(pass_2) < 6:
            raise forms.ValidationError('pass short')
        elif not any(x.isupper() for x in pass_2):      #If there is no small letter in pass_2
            raise forms.ValidationError('pass not big letter')
        return pass_1


class UserLoginForm(forms.Form):
    user = forms.CharField(max_length=20)
    password = forms.CharField(max_length=20)


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'address']

