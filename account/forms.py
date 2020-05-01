from django import forms
from .models import Account


class RegisterForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['username', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['email', 'password']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email Address'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})

        }
