from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account, Follower
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
import datetime, random, hashlib
from random import random
from foodproviders.models import FoodProviders, FollowerProvider
from recipe.models import Recipe, Category, Cuisine, Ingredient, Tags, Comments, Likes, Menus, Menu_Recipe
from account.views import userDetails
from rest_framework.authtoken.models import Token


def become_fp(request):

    token, _ = Token.objects.get_or_create(user=request.user)

    args = {'title': "Become Food Provider",
            'left_menu_selected': 'become_fp',
            'uDetails': userDetails(request),
            'token': token
            }
    return render(request, 'foodproviders/become_fp.html', args)


def providerPage(request, provider_id,  *args, **kwargs):

    provider = FoodProviders.objects.get(id=provider_id)

    recipes_all = Recipe.objects.filter(recipe_food_provider=provider_id).order_by('-id')
    is_following_by_me = FollowerProvider.objects.filter(followerProvider=request.user, targetProvider=provider).count()

    recipes_all_temp = []
    for each in recipes_all:
        each.like_count = Likes.objects.filter(recipe_id=each.id).count()
        each.comment_count = Comments.objects.filter(recipe_id=each.id).count()
        each.liked = Likes.objects.filter(recipe_id=each.id, like_user=request.user).count()
        recipes_all_temp.append(each)

    args = {
            'uDetails': userDetails(request),
            'provider': provider,
            'provider_recipe_count': Recipe.objects.filter(recipe_food_provider=provider.id).count(),
            'otheruser_menu_count': Menus.objects.filter(menu_provider=provider).count(),
            'provider_follower_count': FollowerProvider.objects.filter(targetProvider=provider.id).count(),
            'is_following_by_me' : is_following_by_me,
            'recipes_all': recipes_all_temp
            }
    return render(request, 'foodproviders/provider_page.html', args)


def providerMenus(request, provider_id,  *args, **kwargs):

    provider = FoodProviders.objects.get(id=provider_id)
    is_following_by_me = FollowerProvider.objects.filter(followerProvider=request.user, targetProvider=provider).count()
    token, _ = Token.objects.get_or_create(user=request.user)

    menus_all = Menus.objects.filter(menu_provider=provider).order_by('-id')
    menus_all_temp = []
    for each in menus_all:
        added_recipes = Menu_Recipe.objects.filter(menu_id=each.id)
        each.recipes = added_recipes

        added_recipe_ids = []
        for e in added_recipes:
            added_recipe_ids.append(e.recipe_id.id)

        each.other_recipes = Recipe.objects.filter(recipe_food_provider=provider).exclude(id__in=added_recipe_ids)
        menus_all_temp.append(each)

    args = {
            'uDetails': userDetails(request),
            'provider': provider,
            'provider_recipe_count': Recipe.objects.filter(recipe_food_provider=provider.id).count(),
            'otheruser_menu_count': Menus.objects.filter(menu_provider=provider).count(),
            'provider_follower_count': FollowerProvider.objects.filter(targetProvider=provider.id).count(),
            'is_following_by_me': is_following_by_me,
            'menus_all': menus_all_temp,
            'token': token
            }
    return render(request, 'foodproviders/provider_menus.html', args)



def providerSettings(request, provider_id,  *args, **kwargs):
    provider = FoodProviders.objects.get(id=provider_id)
    token, _ = Token.objects.get_or_create(user=request.user)
    args = {'title': "Provider Settings",
            'left_menu_selected': '',
            'provider': provider,
            'token': token,
            'uDetails': userDetails(request)
            }
    return render(request, 'foodproviders/settings.html', args)


def providerFollowers(request, provider_id,  *args, **kwargs):
    provider = FoodProviders.objects.get(id=provider_id)
    is_following_by_me = FollowerProvider.objects.filter(followerProvider=request.user, targetProvider=provider).count()
    token, _ = Token.objects.get_or_create(user=request.user)

    users = FollowerProvider.objects.filter(targetProvider=provider_id)
    users2_temp = []
    for each in users:
        follower_count = Follower.objects.filter(target=each.followerProvider).count()
        recipe_count = Recipe.objects.filter(recipe_user=each.followerProvider).count()

        each.extra = str(recipe_count) + " recipes, " + str(follower_count) + " followers"
        users2_temp.append(each)

    args = {
        'uDetails': userDetails(request),
        'provider': provider,
        'provider_recipe_count': Recipe.objects.filter(recipe_food_provider=provider.id).count(),
        'otheruser_menu_count': Menus.objects.filter(menu_provider=provider).count(),
        'provider_follower_count': FollowerProvider.objects.filter(targetProvider=provider.id).count(),
        'is_following_by_me': is_following_by_me,
        'users': users2_temp,
        'token': token
    }
    return render(request, 'foodproviders/provider_followers.html', args)