from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import json
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from .models import Account
from recipe.models import Recipe
from rest_framework.authtoken.models import Token


def user_signup(request,  *args, **kwargs):
    if request.method == 'POST':

        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('username')

        #check if user exist
        user_email_check = Account.objects.filter(email=email).count()
        user_username_check = Account.objects.filter(username=username).count()

        if user_email_check == 0 and user_username_check == 0:

            user = Account
            user.objects.create_user(email, username, password)

            user = authenticate(email=email, password=password)

            django_login(request, user)

            arg = {'authenticated': True, 'gelen': "hut"}
            return HttpResponse(json.dumps(arg), content_type="application/json")
        else:
            print("------")
            arg = {'authenticated': False}
            return HttpResponse(json.dumps(arg), content_type="application/json")

    else:

        args = {}
        return render(request, 'accounts/signup.html', args)


def user_login(request, *args, **kwargs):
    if request.method == 'POST':

        email = request.POST.get('email')
        raw_password = request.POST.get('password')

        user = authenticate(email=email, password=raw_password)


        if user is not None and user.is_active:
            django_login(request, user)

            arg = {'authenticated': True}
            return HttpResponse(json.dumps(arg), content_type="application/json")

        else:
            arg = {'authenticated': False}
            return HttpResponse(json.dumps(arg), content_type="application/json")

    else:
        args = {}
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
        recipe_count = Recipe.objects.filter(recipe_user=request.user.id).count()
        notification_count = 0
    else:
        is_auth = False
        user_name = ""
        birth_day = ""
        gender = ""
        password = ""
        email_address = ""
        profile_photo = ""
        recipe_count = 0
        notification_count = 0

    return {'is_auth': is_auth, 'notification_count': notification_count, 'recipe_count': recipe_count, 'user_name': user_name, 'email_address': email_address, 'birth_day': birth_day,
            'gender': gender, 'password': password, 'profile_photo': profile_photo}

