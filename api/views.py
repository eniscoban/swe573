from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST
from recipe.models import Recipe, Category, Cuisine, Ingredient, Nutrients, Tags, Comments, Likes, Menus, Menu_Recipe
from account.models import Account, Follower
from foodproviders.models import FoodProviders, FollowerProvider
from api.serializers import RecipeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import json, random, datetime
import requests



# Register user via email, username and password.
# After recording, it returns generated token
# It also create a session for client
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def register(request):
    try:
        email = request.data['email']
        password = request.data['password']
        username = request.data['username']
    except:
        return Response({'error': 'Please provide correct email and password'}, status=HTTP_400_BAD_REQUEST)

    user = Account
    user.objects.create_user(email,username,password)
    user = authenticate(email=email, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        request.session['wwwe'] = token.key
        return Response({'authenticated': True, 'token': "Token " + token.key})
    else:
        return Response({'authenticated': False, 'token': None})


# needs valid email adn password.
# It returns generated token
# It also create a session for client
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def login(request):
    try:
        email = request.data['email']
        password = request.data['password']
    except:
        return Response({'error': 'Please provide correct email and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(email=email, password=password)
    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        request.session['wwwe'] = token.key
        return Response({'authenticated': True, 'token': "Token " + token.key})
    else:
        return Response({'authenticated': False, 'token': None})

# listst member's recipes
@csrf_exempt
@api_view(["POST"])
def list_my_recipes(request):
    user = Token.objects.get(key=request.auth).user
    recipes = Recipe.objects.filter(recipe_user=user.id)
    serializer = RecipeSerializer(recipes, many=True)
    return JsonResponse(serializer.data, safe=False)


@csrf_exempt
@api_view(["GET"])
def list_all_recipes(request):
    recipes = Recipe.objects.all()
    serializer = RecipeSerializer(recipes, many=True)
    return JsonResponse(serializer.data, safe=False)


# creates recipe with given name, category,cuisine, ingredients and nutrients
# user can post recipe for himself or for the provider he created before
# returns added recipe id for redirection
@csrf_exempt
@api_view(["POST"])
def create_recipe(request):
    user = Token.objects.get(key=request.auth).user
    recipe_name = request.data['recipe_name']
    user_select = request.data['user_select']
    recipe_description = request.POST.get('recipe_description')
    recipe_category = request.data['recipe_category']
    recipe_cuisine = request.data['recipe_cuisine']
    recipe_serving = request.data['recipe_serving']
    tags = json.loads(request.POST.get('tags'))
    ingredients = json.loads(request.POST.get('ingredients'))
    nutrients = json.loads(request.POST.get('nutrients'))

    recipe_cuisine1 = Cuisine.objects.get(id=recipe_cuisine)
    recipe_category1 = Category.objects.get(id=recipe_category)

    try:
        provider = FoodProviders.objects.get(id=user_select)
    except FoodProviders.DoesNotExist:
        provider = None

    newRecipe = Recipe(
        recipe_name=recipe_name,
        recipe_user=user,
        recipe_food_provider=provider,
        recipe_description=recipe_description,
        recipe_cuisine=recipe_cuisine1,
        recipe_category=recipe_category1,
        how_many_person=recipe_serving,
        added_date=datetime.datetime.now()
    )
    newRecipe.save(force_insert=True)

    newRecipeSec = Recipe.objects.get(id=newRecipe.id)

    for each in ingredients:
        newIngredient = Ingredient(ingredient_name=each['name'], recipe_id=newRecipeSec)
        newIngredient.save()

    for each in nutrients:
        newNutrients = Nutrients(
            nutrient_name=each['nutrient_name'],
            nutrient_unit=each['nutrient_unit'],
            nutrient_quantity=each['nutrient_amount'],
            recipe_id=newRecipeSec)
        newNutrients.save()

    for each in tags:
        newTags = Tags(
            tag_name=each['name'],
            tag_tid=each['tid'],
            recipe_id=newRecipeSec)
        newTags.save()

    data = {
        'newRecipeSec': newRecipeSec.id,
        'success': True
    }
    return JsonResponse(data)

#adds comment for recipe
@csrf_exempt
@api_view(["POST"])
def add_comment(request):
    user = Token.objects.get(key=request.auth).user
    comment = request.data['comment']
    recipe_id = request.data['recipe_id']
    recipe = Recipe.objects.get(id=recipe_id)

    newComment = Comments(
        comment=comment,
        comment_user=user,
        recipe_id=recipe,
        added_date=datetime.datetime.now()
    )
    newComment.save(force_insert=True)
    data = {
       # 'newComment': newComment.id,
        'comment': comment,
        'comment_user': user.username,
        'added_date': datetime.datetime.now()
    }
    return JsonResponse(data)


@csrf_exempt
@api_view(["POST"])
def follow_user(request):
    user = Token.objects.get(key=request.auth).user
    target_username = request.data['target_username']
    target = Account.objects.get(username=target_username)
    newFollow = Follower(
        target=target,
        follower=user
    )
    newFollow.save(force_insert=True)
    data = {'success': True}
    return JsonResponse(data)

@csrf_exempt
@api_view(["POST"])
def unfollow_user(request):
    user = Token.objects.get(key=request.auth).user
    target_username = request.data['target_username']
    target = Account.objects.get(username=target_username)
    Follower.objects.filter(target=target, follower=user).delete()
    data = {'success': True}
    return JsonResponse(data)


@csrf_exempt
@api_view(["POST"])
def like_recipe(request):

    user = Token.objects.get(key=request.auth).user
    recipe_id = request.data['recipe_id']
    recipe = Recipe.objects.get(id=recipe_id)

    newLike = Likes(
        like_user=user,
        recipe_id=recipe,
        added_date=datetime.datetime.now()
    )
    newLike.save(force_insert=True)
    data = {'success': True}
    return JsonResponse(data)


@csrf_exempt
@api_view(["POST"])
def unlike_recipe(request):
    user = Token.objects.get(key=request.auth).user
    recipe_id = request.data['recipe_id']
    recipe = Recipe.objects.get(id=recipe_id)
    Likes.objects.filter(recipe_id=recipe, like_user=user).delete()
    data = { 'success': True }
    return JsonResponse(data)


# Creates food provider page for user.
# latitude and longitude values must be recorded as Point after Geo features added.
# Returns added page id for redirection
@csrf_exempt
@api_view(["POST"])
def create_foodprovider(request):
    user = Token.objects.get(key=request.auth).user
    page_name = request.data['page_name']
    page_description = request.POST.get('page_description')
    page_address = request.data['page_address']
    longitude = request.data['longitude']
    latitude = request.data['latitude']

    newProvider = FoodProviders(
        provider_name=page_name,
        provider_user=user,
        provider_description=page_description,
        provider_address=page_address,
        provider_lat=longitude,
        provider_long=latitude,
        added_date=datetime.datetime.now()
    )
    newProvider.save(force_insert=True)

    newProviderSec = FoodProviders.objects.get(id=newProvider.id)
    data = {
            'provider_id': newProviderSec.id,
            'success': True
        }
    return JsonResponse(data)

@csrf_exempt
@api_view(["POST"])
def edit_foodprovider(request):
    user = Token.objects.get(key=request.auth).user

    provider_id = request.data['provider_id']
    page_name = request.data['page_name']
    page_description = request.POST.get('page_description')
    page_address = request.data['page_address']
    longitude = request.data['longitude']
    latitude = request.data['latitude']

    prv = FoodProviders.objects.get(id=provider_id)

    prv.provider_name = page_name
    prv.provider_description = page_description
    prv.provider_address = page_address
    prv.provider_lat = longitude
    prv.provider_long = latitude

    prv.save()

    data = {
        'provider_id': provider_id,
        'success': True
    }
    return JsonResponse(data)

# only food providers can create menu
# name and provider is needed
@csrf_exempt
@api_view(["POST"])
def createMenu(request):
    user = Token.objects.get(key=request.auth).user
    menu_name = request.data['menu_name']
    food_provider_id = request.data['food_provider_id']

    prv = FoodProviders.objects.get(id=food_provider_id)

    newMenu = Menus(
        menu_name=menu_name,
        menu_provider=prv
    )
    newMenu.save(force_insert=True)

    data = {'success': True }
    return JsonResponse(data)


@csrf_exempt
@api_view(["POST"])
def addToMenu(request):
    menu_id = request.data['menu_id']
    recipe_id_will_add = request.data['recipe_id_will_add']

    mm = Menus.objects.get(id=menu_id)
    rr = Recipe.objects.get(id=recipe_id_will_add)

    newMenu_Recipe = Menu_Recipe(
        menu_id=mm,
        recipe_id=rr
    )
    newMenu_Recipe.save(force_insert=True)
    data = {'success': True }
    return JsonResponse(data)


@csrf_exempt
@api_view(["POST"])
def removeFromMenu(request):
    menu_id = request.data['menu_id']
    recipe_id_will_remove = request.data['recipe_id_will_remove']

    mm = Menus.objects.get(id=menu_id)
    rr = Recipe.objects.get(id=recipe_id_will_remove)

    Menu_Recipe.objects.filter(menu_id=mm, recipe_id=rr).delete()

    data = {
        'success': True
    }
    return JsonResponse(data)



@csrf_exempt
@api_view(["POST"])
def follow_provider(request):
    user = Token.objects.get(key=request.auth).user
    target_provider = request.data['target_provider']
    target = FoodProviders.objects.get(id=target_provider)
    newFollow = FollowerProvider(
        targetProvider=target,
        followerProvider=user
    )
    newFollow.save(force_insert=True)

    data = {
        'success': True
    }
    return JsonResponse(data)

@csrf_exempt
@api_view(["POST"])
def unfollow_provider(request):

    user = Token.objects.get(key=request.auth).user
    target_provider = request.data['target_provider']

    target = FoodProviders.objects.get(id=target_provider)

    FollowerProvider.objects.filter(targetProvider=target, followerProvider=user).delete()

    data = {'success': True}
    return JsonResponse(data)


# users can change their avatars
# there are only 9 different avatar
# for next release, uploading photo feature should be added
@csrf_exempt
@api_view(["POST"])
def change_avatar(request):
    avatars = ['prf_1.png', 'prf_2.png', 'prf_3.png', 'prf_4.png', 'prf_5.png', 'prf_6.png',
               'prf_7.png', 'prf_8.png', 'prf_9.png']
    user = Token.objects.get(key=request.auth).user
    user.profile_photo = random.choice(avatars)
    user.save()
    data = {'success': True}
    return JsonResponse(data)

# Requests to wikidata doen't need a secretkey
# Response redirected to relevant javascript as output
@csrf_exempt
@api_view(["POST"])
def getTagsFromWikidata(request):
    keyword = request.data['keyword']
    user = Token.objects.get(key=request.auth).user
    url = "https://wikidata.org/w/api.php?action=wbsearchentities&search=" + keyword + "&format=json&language=en&type=item&continue=0"
    response = requests.get(url)
    #print(response.content)
    #data = {'success': True}
    return HttpResponse(response.content)

