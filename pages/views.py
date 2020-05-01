from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account
from .forms import GeneralSettingsForm, PassSettingsForm
from django.urls import reverse
from django.contrib import messages


def userDetails(request):
    if request.user.is_authenticated:
        is_auth = True
        user_name = request.user.username
        birth_day = request.user.date_birth
        gender = request.user.gender
        password = request.user.password
    else:
        is_auth = False
        user_name = ""
        birth_day = ""
        gender = ""
        password = ""
    return {'is_auth': is_auth, 'user_name': user_name, 'birth_day': birth_day, 'gender': gender, 'password': password}


def home(request):
    uDetails = userDetails(request)
    args = {'title': "Home Title",
            'left_menu_selected': 'feed',
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name']
            }
    return render(request, 'pages/home.html', args)


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


def settings_email(request):
    form = PassSettingsForm()
    uDetails = userDetails(request)
    args = {'title': "Settings",
            'left_menu_selected': 'settings',
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name'],
            'form': form
            }
    return render(request, 'pages/settings_password.html', args)


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
        form = GeneralSettingsForm(user_name=uDetails['user_name'], gender=uDetails['gender'], birth_day=uDetails['birth_day'])

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
