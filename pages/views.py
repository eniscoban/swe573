from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from account.models import Account, Follower
from .forms import GeneralSettingsForm, PassSettingsForm
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
import datetime, random, hashlib
from random import random
from recipe.models import Recipe, Category, Cuisine, Ingredient, Tags, Comments, Likes
from django.db.models import Q
from account.views import userDetails
from foodproviders.views import FoodProviders, FollowerProvider
from rest_framework.authtoken.models import Token


def home(request):
    if request.user.is_authenticated:

        users = Follower.objects.filter(follower=request.user)
        users_followed = []
        for each in users:
            users_followed.append(each.target.id)

        providers = FollowerProvider.objects.filter(followerProvider=request.user)
        providers_followed = []
        for each in providers:
            providers_followed.append(each.targetProvider.id)


        recipes_all = Recipe.objects.filter(Q(recipe_user__in=users_followed) | Q(recipe_food_provider__in=providers_followed)).order_by('-id')
        recipes_all_temp = []

        for each in recipes_all:
            each.like_count = Likes.objects.filter(recipe_id=each.id).count()
            each.comment_count = Comments.objects.filter(recipe_id=each.id).count()
            each.liked = Likes.objects.filter(recipe_id=each.id, like_user=request.user).count()
            recipes_all_temp.append(each)

        args = {'title': "Home Title",
                'left_menu_selected': 'feed',
                'uDetails': userDetails(request),
                'recipes_all': recipes_all_temp

                }
        return render(request, 'pages/home.html', args)
    else:
        return HttpResponseRedirect(reverse('user_login'))


def create_recipe(request):
    categories = Category.objects.all()
    cuisines = Cuisine.objects.all()
    token, _ = Token.objects.get_or_create(user=request.user)
    providers = FoodProviders.objects.filter(provider_user=request.user)

    args = {'title': "Create Recipe",
            'uDetails': userDetails(request),
            'categories': categories,
            'cuisines': cuisines,
            'providers': providers,
            'token': token
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
    recipes_all = Recipe.objects.filter(recipe_user=request.user.id).order_by('-id')
    recipes_all_temp = []
    for each in recipes_all:
        each.like_count = Likes.objects.filter(recipe_id=each.id).count()
        each.comment_count = Comments.objects.filter(recipe_id=each.id).count()
        each.liked = Likes.objects.filter(recipe_id=each.id, like_user=request.user).count()
        recipes_all_temp.append(each)

    args = {'title': "My Recipe",
            'left_menu_selected': 'my_recipes',
            'uDetails': userDetails(request),
            'recipes_all': recipes_all_temp
            }
    return render(request, 'pages/my_recipes.html', args)


def search(request,  *args, **kwargs):

    recipes_all_temp = []
    keyword = request.GET.get('keyword')

    recipes_keyword = Recipe.objects.filter(recipe_name__contains=keyword).order_by('-id')
    for each in recipes_keyword:
        each.like_count = Likes.objects.filter(recipe_id=each.id).count()
        each.comment_count = Comments.objects.filter(recipe_id=each.id).count()
        each.liked = Likes.objects.filter(recipe_id=each.id, like_user=request.user).count()
        recipes_all_temp.append(each)


    args = {'title': "Search Recipe",
            'left_menu_selected': '',
            'uDetails': userDetails(request),
            'keyword': keyword,
            'recipes_all': recipes_all_temp
            }
    return render(request, 'pages/search.html', args)

def cuisine(request, cuisine_id):
    recipes_all = Recipe.objects.filter(recipe_cuisine=cuisine_id).order_by('-id')
    cuis = Cuisine.objects.get(id=cuisine_id)

    args = {'title': "My Recipe",
            'left_menu_selected': '',
            'uDetails': userDetails(request),
            'cuisine_name': cuis.cuisine_name,
            'recipes_all': recipes_all
            }
    return render(request, 'pages/cuisine.html', args)


def category(request, category_id):
    recipes_all = Recipe.objects.filter(recipe_category=category_id).order_by('-id')
    cat = Category.objects.get(id=category_id)

    args = {'title': "My Recipe",
            'left_menu_selected': '',
            'uDetails': userDetails(request),
            'category_name': cat.category_name,
            'recipes_all': recipes_all
            }
    return render(request, 'pages/category.html', args)


def tag(request, tag_id):
    tag_recipeid = Tags.objects.filter(tag_tid=tag_id)

    arr = []
    for each in tag_recipeid:
        arr.append(each.recipe_id.id)

    recipes_all = Recipe.objects.filter(id__in=arr).order_by('-id')

    tag_name = Tags.objects.filter(tag_tid=tag_id)[:1]

    args = {'title': "",
            'left_menu_selected': '',
            'uDetails': userDetails(request),
            'tag_name': tag_name[0],
            'recipes_all': recipes_all
            }
    return render(request, 'pages/tag.html', args)


def notifications(request):
    args = {'title': "Notifications",
            'left_menu_selected': 'notifications',
            'uDetails': userDetails(request)
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

        args = {'title': "Settings",
                'left_menu_selected': 'settings',
                'uDetails': userDetails(request)
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

        args = {'title': "Change Password",
                'left_menu_selected': 'settings',
                'uDetails': userDetails(request)

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
                                   birth_day=uDetails['birth_day'], about=uDetails['about'])

        # create and save token for api
        token, _ = Token.objects.get_or_create(user=request.user)

        args = {'title': "Settings",
                'left_menu_selected': 'settings',
                'uDetails': uDetails,
                'token': token,
                'my_recipe_count': uDetails['recipe_count'],
                'my_notification_count': uDetails['notification_count'],
                'form': form
                }
        return render(request, 'pages/settings.html', args)


def my_followers(request):
    users = Follower.objects.filter(target=request.user)
    users2_temp = []
    for each in users:
        # each.follower.is_following_by_me = Follower.objects.filter(follower=request.user, target=each.follower).count()

        follower_count = Follower.objects.filter(target=each.follower).count()
        recipe_count = Recipe.objects.filter(recipe_user=each.follower).count()

        each.extra = str(recipe_count) + " recipes, " + str(follower_count) + " followers"
        users2_temp.append(each)

    args = {'title': "My Followers",
            'left_menu_selected': 'followers',
            'uDetails': userDetails(request),
            'users': users2_temp
            }

    return render(request, 'pages/my_followers.html', args)


def my_followings(request):
    users = Follower.objects.filter(follower=request.user)
    users2_temp = []
    for each in users:
        follower_count = Follower.objects.filter(target=each.target).count()
        recipe_count = Recipe.objects.filter(recipe_user=each.target).count()

        each.extra = str(recipe_count) + " recipes, " + str(follower_count) + " followers"
        users2_temp.append(each)

    args = {'title': "My Followings",
            'left_menu_selected': 'followings',
            'uDetails': userDetails(request),
            'users': users2_temp
            }
    return render(request, 'pages/my_followings.html', args)


def my_following_providers(request):
    providers = FollowerProvider.objects.filter(followerProvider=request.user)
    providers_temp = []
    for each in providers:
        follower_count = FollowerProvider.objects.filter(targetProvider=each.targetProvider).count()
        recipe_count = Recipe.objects.filter(recipe_food_provider=each.targetProvider).count()

        each.extra = str(recipe_count) + " recipes, " + str(follower_count) + " followers"
        providers_temp.append(each)


    args = {'title': "My Following Providers",
            'left_menu_selected': 'following_providers',
            'uDetails': userDetails(request),
            'providers': providers_temp
            }
    return render(request, 'pages/my_following_providers.html', args)


def validate_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': Account.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


def providers_near_me(request):
    args = {'title': "My Followings",
            'left_menu_selected': 'followings',
            'uDetails': userDetails(request)

            }
    return render(request, 'pages/providers_near_me.html', args)
