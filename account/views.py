from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse


def user_signup(request):
    args = {}
    return render(request, 'accounts/signup.html', args)


def user_login(request):
    args = {}
    return render(request, 'accounts/login.html', args)


def logout(request):
    del request.session['wwwe']
    return HttpResponseRedirect(reverse('user_login'))
