from django.contrib.auth import authenticate
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.status import HTTP_400_BAD_REQUEST
from recipe.models import Recipe
from account.models import Account
from api.serializers import RecipeSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

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


def userDetails(request, token):
    user = Token.objects.get(key=token).user

    is_auth = True
    user_id = user.id
    user_name = user.username
    birth_day = user.date_birth
    gender = user.gender
    password = user.password
    email_address = user.email
    profile_photo = user.profile_photo

    return {'is_auth': is_auth, 'user_id': user_id, 'user_name': user_name, 'email_address': email_address, 'birth_day': birth_day,
            'gender': gender, 'password': password, 'profile_photo': profile_photo}


def recipe_count(request):

    #user = Token.objects.get(key=request.auth).user
    #return Recipe.objects.filter(recipe_user=user.id).count()
    return 3


@csrf_exempt
@api_view(["POST"])
def list_my_recipes(request):
    print("-------------sss--------------")
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
