from django import forms
from account.models import Account
from django.forms import fields, CheckboxInput
from django.shortcuts import render, redirect, get_object_or_404


class PassSettingsForm(forms.Form):

    fields = ['pass1', 'pass2', 'pass3']
    widgets = {
        'pass1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        'pass2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        'pass3': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})

    }



class EmailSettingsForm(forms.ModelForm):
    emailF = forms.EmailInput()

    widgets = {
        'emailF': forms.TextInput()
    }




class GeneralSettingsForm(forms.ModelForm):
    username_hidden = forms.CharField(widget=forms.HiddenInput(), required=False)

    def __init__(self, *args, **kwargs):
        self.user_name = kwargs.pop('user_name', '')
        self.gender = kwargs.pop('gender', '')
        self.birth_day = kwargs.pop('birth_day', '')
        self.about = kwargs.pop('about', '')

        super(GeneralSettingsForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget = forms.TextInput(
            attrs={'value': self.user_name, 'class': 'form-control', 'placeholder': 'Username'})

        self.fields['gender'].initial = self.gender
        self.fields['date_birth'].widget = forms.DateInput(
            attrs={'type': 'date', 'value': self.birth_day, 'class': 'form-control', 'placeholder': 'Birth Day'})
        self.fields['username_hidden'].widget = forms.HiddenInput(attrs={'value': self.user_name})
        self.fields['about'].widget = forms.Textarea(
            attrs={'rows':"3", 'class': 'form-control', 'placeholder': 'About yourself'})
        self.fields['about'].initial = self.about


    class Meta:
        model = Account
        CHOICES = (('Female', 'Female',), ('Male', 'Male',))
        fields = ['username', 'date_birth', 'gender', 'about']

        widgets = {
            'date_birth': forms.DateInput(
                attrs={'type': 'date', 'value': '2011-08-19', 'class': 'form-control', 'placeholder': 'Birth Day'}),
            'gender': forms.Select(choices=CHOICES, attrs={'class': 'form-control'})
        }
