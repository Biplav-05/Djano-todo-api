# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2']
        
class OtpForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['otp']
