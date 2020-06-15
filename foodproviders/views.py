from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account, Follower
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
import datetime, random, hashlib
from random import random
from foodproviders.models import FoodProviders
from recipe.models import Recipe, Category, Cuisine, Ingredient, Tags, Comments, Likes
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

    #recipes_all = Recipe.objects.filter(recipe_user=otheruser.id).order_by('-id')
    #is_following_by_me = Follower.objects.filter(follower=request.user, target=otheruser).count()

    #recipes_all_temp = []
    #for each in recipes_all:
        #each.like_count = Likes.objects.filter(recipe_id=each.id).count()
        #each.comment_count = Comments.objects.filter(recipe_id=each.id).count()
        #each.liked = Likes.objects.filter(recipe_id=each.id, like_user=request.user).count()
        #recipes_all_temp.append(each)

    args = {
            'uDetails': userDetails(request),
            'provider': provider,
            #'provider_recipe_count': Recipe.objects.filter(recipe_user=otheruser.id).count(),
            #'provider_follower_count': Follower.objects.filter(target=otheruser.id).count(),
            #'is_following_by_me' : is_following_by_me,
            #'recipes_all': recipes_all_temp
            }
    return render(request, 'foodproviders/provider_page.html', args)