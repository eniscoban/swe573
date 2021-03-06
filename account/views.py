from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import json
from django.contrib.auth import authenticate
from django.contrib.auth import login as django_login
from django.contrib.auth import logout as django_logout
from .models import Account, Follower
from recipe.models import Recipe, Likes, Comments
from foodproviders.models import FoodProviders, FollowerProvider
from rest_framework.authtoken.models import Token


'''
Register page view. Creates an Account object which is a custom User class
Authentication is based on email and password. 
Needs email, username and password.  
'''
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

'''
Login page view. Checks if user exist or not. 
Authentication is based on email and password. 
Needs email, username and password.  
'''
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

#logout method , clears session
def logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('home'))

'''
A common function that returns all user details. 
It is imported by many other page.
'''
def userDetails(request):

    if request.user.is_authenticated:
        token, _ = Token.objects.get_or_create(user=request.user)
        is_auth = True
        user_name = request.user.username
        birth_day = request.user.date_birth
        gender = request.user.gender
        password = request.user.password
        email_address = request.user.email
        profile_photo = request.user.profile_photo
        about = request.user.about
        recipe_count = Recipe.objects.filter(recipe_user=request.user.id).count()
        notification_count = 0
        my_follower_count = Follower.objects.filter(target=request.user.id).count()
        my_following_count = Follower.objects.filter(follower=request.user.id).count()
        my_following_provider_count = FollowerProvider.objects.filter(followerProvider=request.user.id).count()
        providers = FoodProviders.objects.filter(provider_user=request.user.id)
    else:
        is_auth = False
        user_name = ""
        birth_day = ""
        gender = ""
        password = ""
        email_address = ""
        profile_photo = ""
        recipe_count = 0
        about = ""
        notification_count = 0
        my_follower_count = 0
        my_following_count = 0
        my_following_provider_count = 0
        token = ""
        providers = []

    return {'is_auth': is_auth,
            'my_follower_count': my_follower_count,
            'my_following_count': my_following_count,
            'my_following_provider_count': my_following_provider_count,
            'notification_count': notification_count,
            'recipe_count': recipe_count,
            'user_name': user_name,
            'email_address': email_address,
            'birth_day': birth_day,
            'gender': gender,
            'password': password,
            'profile_photo': profile_photo,
            'about': about,
            'providers': providers,
            'token': token
            }


# This view is used when client want to display another users page.
# like_count, comment_count and liked values added extra to recipe object.
def userPage(request, user_name,  *args, **kwargs):

    otheruser = Account.objects.get(username=user_name)

    if otheruser == request.user:
        return redirect('/settings/')
    else:

        recipes_all = Recipe.objects.filter(recipe_user=otheruser.id).order_by('-id')
        is_following_by_me = Follower.objects.filter(follower=request.user, target=otheruser).count()

        recipes_all_temp = []
        for each in recipes_all:
            each.like_count = Likes.objects.filter(recipe_id=each.id).count()
            each.comment_count = Comments.objects.filter(recipe_id=each.id).count()
            # if client liked recipe or not
            each.liked = Likes.objects.filter(recipe_id=each.id, like_user=request.user).count()
            recipes_all_temp.append(each)

        args = {
                'uDetails': userDetails(request),
                'otheruser': otheruser,
                'otheruser_recipe_count': Recipe.objects.filter(recipe_user=otheruser.id).count(),
                'otheruser_follower_count': Follower.objects.filter(target=otheruser.id).count(),
                'otheruser_provider_count': FoodProviders.objects.filter(provider_user=otheruser.id).count(),
                'is_following_by_me' : is_following_by_me,
                'recipes_all': recipes_all_temp
                }
        return render(request, 'pages/user_page.html', args)


# Displays follower users of client
def userFollowers(request, user_name,  *args, **kwargs):

    otheruser = Account.objects.get(username=user_name)
    recipes_all = Recipe.objects.filter(recipe_user=otheruser.id).order_by('-id')

    is_following_by_me = Follower.objects.filter(follower=request.user, target=otheruser).count()

    users = Follower.objects.filter(target=otheruser.id)
    users2_temp = []
    for each in users:
        follower_count = Follower.objects.filter(target=each.follower).count()
        recipe_count = Recipe.objects.filter(recipe_user=each.follower).count()
        #extra information about listed user
        each.extra = str(recipe_count) + " recipes, " + str(follower_count) + " followers"
        users2_temp.append(each)

    args = {
        'uDetails': userDetails(request),
        'otheruser': otheruser,
        'otheruser_recipe_count': Recipe.objects.filter(recipe_user=otheruser.id).count(),
        'otheruser_follower_count': Follower.objects.filter(target=otheruser.id).count(),
        'otheruser_provider_count': FoodProviders.objects.filter(provider_user=otheruser.id).count(),
        'is_following_by_me': is_following_by_me,
        'users': users2_temp
    }
    return render(request, 'pages/user_followers.html', args)

'''
Lists food providers which are created by user himself.
They are listed at users profile pages as tab
'''
def userProviders(request, user_name,  *args, **kwargs):

    otheruser = Account.objects.get(username=user_name)
    recipes_all = Recipe.objects.filter(recipe_user=otheruser.id).order_by('-id')

    #if user follows provider or not
    is_following_by_me = Follower.objects.filter(follower=request.user, target=otheruser).count()

    providers = FoodProviders.objects.filter(provider_user=otheruser.id)
    providers_temp = []
    for each in providers:
        follower_count = FollowerProvider.objects.filter(targetProvider=each).count()
        recipe_count = Recipe.objects.filter(recipe_food_provider=each).count()
        #extra information about provider
        each.extra = str(recipe_count) + " recipes, " + str(follower_count) + " followers"
        providers_temp.append(each)

    args = {
        'uDetails': userDetails(request),
        'otheruser': otheruser,
        'otheruser_recipe_count': Recipe.objects.filter(recipe_user=otheruser.id).count(),
        'otheruser_follower_count': Follower.objects.filter(target=otheruser.id).count(),
        'otheruser_provider_count': FoodProviders.objects.filter(provider_user=otheruser.id).count(),
        'is_following_by_me': is_following_by_me,
        'providers': providers_temp
    }
    return render(request, 'pages/user_providers.html', args)