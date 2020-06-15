from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST
from recipe.models import Recipe, Category, Cuisine, Ingredient, Nutrients, Tags, Comments, Likes
from account.models import Account, Follower
from foodproviders.models import FoodProviders
from api.serializers import RecipeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import datetime
import json


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


@csrf_exempt
@api_view(["POST"])
def create_recipe(request):

    user = Token.objects.get(key=request.auth).user
    recipe_name = request.data['recipe_name']
    recipe_description = request.POST.get('recipe_description')
    recipe_category = request.data['recipe_category']
    recipe_cuisine = request.data['recipe_cuisine']
    recipe_serving = request.data['recipe_serving']
    tags = json.loads(request.POST.get('tags'))
    ingredients = json.loads(request.POST.get('ingredients'))
    nutrients = json.loads(request.POST.get('nutrients'))

    recipe_cuisine1 = Cuisine.objects.get(id=recipe_cuisine)
    recipe_category1 = Category.objects.get(id=recipe_category)

    newRecipe = Recipe(
        recipe_name=recipe_name,
        recipe_user=user,
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
        'newRecipeSec': "newRecipeSec",
        'user': user.username,
        'recipe_name': recipe_name,
        'recipe_description': recipe_description,
        'ingredients': ingredients[0]['name'],
        'nutrients': nutrients[0]['nutrient_name'],
        'tags': tags[0]['name']

    }
    return JsonResponse(data)


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

    data = {
        'success': True
    }
    return JsonResponse(data)

@csrf_exempt
@api_view(["POST"])
def unfollow_user(request):

    user = Token.objects.get(key=request.auth).user
    target_username = request.data['target_username']

    target = Account.objects.get(username=target_username)

    Follower.objects.filter(target=target, follower=user).delete()

    data = {
        'success': True
    }
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

    data = {
        'success': True
    }
    return JsonResponse(data)


@csrf_exempt
@api_view(["POST"])
def unlike_recipe(request):

    user = Token.objects.get(key=request.auth).user
    recipe_id = request.data['recipe_id']
    recipe = Recipe.objects.get(id=recipe_id)

    Likes.objects.filter(recipe_id=recipe, like_user=user).delete()

    data = {
        'success': True
    }
    return JsonResponse(data)


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
