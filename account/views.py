from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Account
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from django.urls import reverse
from .forms import RegisterForm, LoginForm
from recipe.models import Recipe


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


def userDetails(request):
    if request.user.is_authenticated:
        is_auth = True
        user_name = request.user.username
        birth_day = request.user.date_birth
        gender = request.user.gender
        password = request.user.password
        email_address = request.user.email
        profile_photo = request.user.profile_photo
    else:
        is_auth = False
        user_name = ""
        birth_day = ""
        gender = ""
        password = ""
        email_address = ""
        profile_photo = ""
    return {'is_auth': is_auth, 'user_name': user_name, 'email_address': email_address, 'birth_day': birth_day,
            'gender': gender, 'password': password, 'profile_photo': profile_photo}


def recipe_count(request):
    return Recipe.objects.filter(recipe_user=request.user.id).count()