from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.urls import reverse
from .forms import RegisterForm, LoginForm


def user_signup(request):
    if request.method == 'POST':
        regform = RegisterForm(request.POST)

        if regform.is_valid():
            user = regform.save()
            user.set_password(user.password)
            user.save()

            email = regform.cleaned_data.get('email')
            raw_password = regform.cleaned_data.get('password')

            user = authenticate(email=email, password=raw_password)
            django_login(request, user)
            return HttpResponseRedirect(reverse('home'))

    else:
        form = RegisterForm()
        args = {'form': form}
        return render(request, 'accounts/signup.html', args)


def user_login(request):
    if request.method == 'POST':

        loginform = LoginForm(request.POST)

        email = request.POST.get('email')
        raw_password = request.POST.get('password')

        user = authenticate(email=email, password=raw_password)

        if user is not None and user.is_active:
            django_login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            args = {'err': 'Invalid email or password!'}
            return render(request, 'accounts/login.html', args)

    else:
        form = LoginForm()
        args = {'form': form}
        return render(request, 'accounts/login.html', args)


def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('home'))
