from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST
from recipe.models import Recipe, Category, Cuisine, Ingredient
from account.models import Account
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


    data = {
        'newRecipeSec': "newRecipeSec",
        'user': user.username,
        'recipe_name': recipe_name,
        'recipe_description': recipe_description,
        'ingredients': ingredients[0]['name'],
        'nutrients': nutrients
    }
    return JsonResponse(data)
