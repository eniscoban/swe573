from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account
from .forms import GeneralSettingsForm
from django.urls import reverse


def userDetails(request):
    if request.user.is_authenticated:
        is_auth = True
        user_name = request.user.username
        birth_day = request.user.date_birth
        gender = request.user.gender
    else:
        is_auth = False
        user_name = ""
        birth_day = ""
        gender = ""
    return {'is_auth': is_auth, 'user_name': user_name, 'birth_day': birth_day, 'gender': gender}


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
