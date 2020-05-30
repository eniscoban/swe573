from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account
from .forms import GeneralSettingsForm, PassSettingsForm
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
import datetime, random, hashlib
from random import random
from recipe.models import Recipe, Category, Cuisine, Ingredient
from account.views import userDetails
from rest_framework.authtoken.models import Token
#from api.views import userDetails, recipe_count, list_my_recipes,list_all_recipes

def home(request):

    if request.user.is_authenticated:
        uDetails = userDetails(request)

        args = {'title': "Home Title",
                'left_menu_selected': 'feed',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name'],
                'profile_photo': uDetails['profile_photo'],
                'my_recipe_count': uDetails['recipe_count'],
                'my_notification_count': uDetails['notification_count'],
                }
        return render(request, 'pages/home.html', args)
    else:
        return HttpResponseRedirect(reverse('user_login'))

def create_recipe(request):
    categories = Category.objects.all()
    cuisines = Cuisine.objects.all()
    token, _ = Token.objects.get_or_create(user=request.user)
    uDetails = userDetails(request)


    args = {'title': "Create Recipe",
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name'],
            'profile_photo': uDetails['profile_photo'],
            'my_recipe_count': uDetails['recipe_count'],
            'my_notification_count': uDetails['notification_count'],
            'categories': categories,
            'cuisines': cuisines,
            'token':token
            }
    return render(request, 'pages/create_recipe.html', args)


def create_recipe_ajax(request):
    uDetails = userDetails(request)
    account = Account.objects.get(id=request.user.id)


    recipe_name = request.POST.get('recipe_name')
    recipe_description = request.POST.get('recipe_description')
    recipe_category = request.POST.get('recipe_category')
    recipe_cuisine = request.POST.get('recipe_cuisine')
    recipe_serving = request.POST.get('recipe_serving')
    ingredients_ready = request.POST.getlist('ingredients_ready[]')

    recipe_cuisine = Cuisine.objects.get(id=recipe_cuisine)
    recipe_category = Category.objects.get(id=recipe_category)

    newRecipe = Recipe(
        recipe_name=recipe_name,
        recipe_user=account,
        recipe_description=recipe_description,
        recipe_cuisine=recipe_cuisine,
        recipe_category=recipe_category,
        how_many_person=recipe_serving,
        added_date=datetime.datetime.now()

    )
    newRecipe.save(force_insert=True)

    newRecipeSec = Recipe.objects.get(id=newRecipe.id)

    for each in ingredients_ready:
        newIngredient = Ingredient(ingredient_name=each, recipe_id=newRecipeSec)
        newIngredient.save()

    data = {
        'recipe_name': recipe_name,
        'recipe_description': recipe_description,
        'recipe_category': recipe_category,
        'recipe_cuisine': recipe_cuisine,
        'recipe_serving': recipe_serving,
        'ingredients_ready': ingredients_ready
    }
    return JsonResponse(data)


def my_recipes(request):

    uDetails = userDetails(request)
    recipes_all = Recipe.objects.filter(recipe_user=request.user.id)

    args = {'title': "My Recipe",
            'left_menu_selected': 'my_recipes',
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name'],
            'profile_photo': uDetails['profile_photo'],
            'my_recipe_count': uDetails['recipe_count'],
            'my_notification_count': uDetails['notification_count'],
            'recipes_all': recipes_all
            }
    return render(request, 'pages/my_recipes.html', args)


def notifications(request):
    uDetails = userDetails(request)
    args = {'title': "Notifications",
            'left_menu_selected': 'notifications',
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name'],
            'profile_photo': uDetails['profile_photo'],
            'my_recipe_count': uDetails['recipe_count'],
            'my_notification_count': uDetails['notification_count']
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
        uDetails = userDetails(request)


        args = {'title': "Settings",
                'left_menu_selected': 'settings',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name'],
                'email_address': uDetails['email_address'],
                'profile_photo': uDetails['profile_photo'],
                'my_recipe_count': uDetails['recipe_count'],
                'my_notification_count': uDetails['notification_count'],
                }
        return render(request, 'pages/settings_email.html', args)


def settings_password(request):

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
        uDetails = userDetails(request)

        args = {'title': "Change Password",
                'left_menu_selected': 'settings',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name'],
                'profile_photo': uDetails['profile_photo'],
                'my_recipe_count': uDetails['recipe_count'],
                'my_notification_count': uDetails['notification_count'],

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

        # create and save token for api
        token, _ = Token.objects.get_or_create(user= request.user)

        args = {'title': "Settings",
                'left_menu_selected': 'settings',
                'is_auth': uDetails['is_auth'],
                'user_name': uDetails['user_name'],
                'birth_day': uDetails['birth_day'],
                'profile_photo': uDetails['profile_photo'],
                'gender': uDetails['gender'],
                'token': token,
                'my_recipe_count': uDetails['recipe_count'],
                'my_notification_count': uDetails['notification_count'],
                'form': form
                }
        return render(request, 'pages/settings.html', args)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Account.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def change_avatar(request):
    avatars = ['prf_1.png', 'prf_2.png', 'prf_3.png', 'prf_4.png', 'prf_5.png', 'prf_6.png',
               'prf_7.png', 'prf_8.png', 'prf_9.png']
    request.user.profile_photo = random.choice(avatars)
    request.user.save()
    data = {
        'result': 'success'
    }
    return JsonResponse(data)




