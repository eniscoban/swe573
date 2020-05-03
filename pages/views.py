from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account
from .forms import GeneralSettingsForm, PassSettingsForm
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from random import random
import hashlib


def userDetails(request):
    if request.user.is_authenticated:
        is_auth = True
        user_name = request.user.username
        birth_day = request.user.date_birth
        gender = request.user.gender
        password = request.user.password
        email_address = request.user.email
    else:
        is_auth = False
        user_name = ""
        birth_day = ""
        gender = ""
        password = ""
        email_address = ""
    return {'is_auth': is_auth, 'user_name': user_name, 'email_address': email_address, 'birth_day': birth_day,
            'gender': gender, 'password': password}


def home(request):
    if request.user.is_authenticated:
        uDetails = userDetails(request)
        args = {'title': "Home Title",
                'left_menu_selected': 'feed',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name']
                }
        return render(request, 'pages/home.html', args)
    else:
        return HttpResponseRedirect(reverse('user_login'))


def create_recipe(request):
    uDetails = userDetails(request)
    args = {'title': "Create Recipe",
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name']
            }
    return render(request, 'pages/create_recipe.html', args)


def my_recipes(request):
    uDetails = userDetails(request)
    args = {'title': "My Recipe",
            'left_menu_selected': 'my_recipes',
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name']
            }
    return render(request, 'pages/my_recipes.html', args)


def notifications(request):
    uDetails = userDetails(request)
    args = {'title': "Notifications",
            'left_menu_selected': 'notifications',
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name']
            }
    return render(request, 'pages/notifications.html', args)


def confirm_email(request, email_hash):
    try:
        new_email = Account.objects.get(email_temp_hash=email_hash)
        request.user.email = new_email.email_temp
        request.user.email_temp = ""
        request.user.email_temp_hash = ""
        request.user.save()
        mes = "Your email has been confirmed!"
    except Account.DoesNotExist:
        mes = "No user found!"

    args = {'title': "Confirm Your Email",
            'mes': mes
            }
    return render(request, 'pages/confirm_email.html', args)


def settings_email(request):
    uDetails = userDetails(request)

    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        queryset = Account.objects.filter(email=new_email).count()

        if queryset == 0:
            hash_email = new_email + str(random())
            hash_result = hashlib.md5(hash_email.encode("utf-8")).hexdigest()

            request.user.email_temp_hash = hash_result
            request.user.email_temp = new_email
            request.user.save()

            mess = "Click to confirm your email: http://127.0.0.1:8000/confirm_email/" + hash_result
            send_mail(
                'Please confirm your email address',
                mess,
                'wwwe874555@gmail.com',
                [new_email],
                fail_silently=False,
            )
            messages.success(request, 'A confirmation email has been sent to your new email address.')
        else:
            messages.warning(request, 'This email is being used by another user!')

        return HttpResponseRedirect(reverse('settings_email'))
    else:

        args = {'title': "Settings",
                'left_menu_selected': 'settings',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name'],
                'email_address': uDetails['email_address']
                }
        return render(request, 'pages/settings_email.html', args)


def settings_password(request):
    uDetails = userDetails(request)

    if request.method == 'POST':

        current_password = request.POST.get('pass1')
        next_password = request.POST.get('pass2')

        if request.user.check_password(current_password):

            request.user.set_password(next_password)
            request.user.save()
            messages.success(request, 'Password successfully updated!')
        else:
            messages.warning(request, 'Wrong current password!')

        return HttpResponseRedirect(reverse('settings_password'))
    else:

        args = {'title': "Change Password",
                'left_menu_selected': 'settings',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name']

                }
        return render(request, 'pages/settings_password.html', args)


def settings(request):
    if request.method == 'POST':
        ff = GeneralSettingsForm(request.POST, instance=request.user)
        if ff.is_valid():
            ff.save()
        return HttpResponseRedirect(reverse('settings'))
    else:
        uDetails = userDetails(request)
        form = GeneralSettingsForm(user_name=uDetails['user_name'], gender=uDetails['gender'],
                                   birth_day=uDetails['birth_day'])

        args = {'title': "Settings",
                'left_menu_selected': 'settings',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name'],
                'birth_day': uDetails['birth_day'],
                'gender': uDetails['gender'],
                'form': form
                }
        return render(request, 'pages/settings.html', args)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Account.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
