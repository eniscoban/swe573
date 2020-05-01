from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate

import os



def home(request):

        args = {}
        title = "Home Title"
        args['title'] = title
        users = User.objects.all()
        args['users'] = users
        return render(request, 'pages/home.html', args)



def signup(request):
    return render(request, 'accounts/signup.html')


def login(request):
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'logout.html')
