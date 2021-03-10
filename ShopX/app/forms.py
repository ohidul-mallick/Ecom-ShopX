from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,UsernameField,PasswordChangeForm
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.contrib.auth.models import User

class CustomerRegistrationform(UserCreationForm):
    password1 = forms.CharField(label='Passowrd',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Passowrd',widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}))
    class Meta:
        model=User
        fields=['username','email','password1','password2']
        labels={'email':'Email'}
        widgets={'username':forms.TextInput(attrs={'class':'form-control'})}



class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':True,'class':'form-control'}))

    password = forms.CharField(label=_("Password"),strip=False ,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-control'}))


class MyPasswordChangeForm(PasswordChangeForm):
    old_password=forms.CharField(label=_("Old Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'current-password','autofocus':True,'class':'form-control'}))


    new_password1=forms.CharField(label=_("New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}),help_text=password_validation.password_validators_help_text_html())


    new_password2=forms.CharField(label=_("Confirm New Password"),strip=False,widget=forms.PasswordInput(attrs={'autocomplete':'new-password','class':'form-control'}))
    
