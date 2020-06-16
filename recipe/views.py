from django.db.models import Sum,Count
from django.shortcuts import render
from account.views import userDetails
from recipe.models import Recipe, Ingredient, Nutrients, Tags, Comments, Likes
from rest_framework.authtoken.models import Token



def recipe(request, recipe_id):

    recipeDetails = Recipe.objects.get(id=recipe_id)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_id)
    comments = Comments.objects.filter(recipe_id=recipe_id).order_by('-id')
    like_count = Likes.objects.filter(recipe_id=recipe_id).count()
    liked = Likes.objects.filter(recipe_id=recipe_id, like_user=request.user).count()

    nutrients = Nutrients.objects.filter(recipe_id=recipe_id)\
        .values('nutrient_name', 'nutrient_unit')\
        .annotate(dcount=Sum('nutrient_quantity'))\
        .order_by('-dcount')

    tags = Tags.objects.filter(recipe_id=recipe_id)

    token, _ = Token.objects.get_or_create(user=request.user)

    args = {'title': "Recipe",
            'left_menu_selected': '',
            'uDetails': userDetails(request),
            'recipe_id': recipe_id,
            'recipe_user': recipeDetails.recipe_user.username,
            'recipe_user_profile_photo': recipeDetails.recipe_user.profile_photo,
            'recipe_name': recipeDetails.recipe_name,
            'recipe_description': recipeDetails.recipe_description,
            'recipe_category': recipeDetails.recipe_category,
            'recipe_cuisine': recipeDetails.recipe_cuisine,
            'recipe_added_date': recipeDetails.added_date,
            'recipe_how_many_person': recipeDetails.how_many_person,
            'recipe_food_provider': recipeDetails.recipe_food_provider,
            'ingredients': ingredients,
            'nutrients': nutrients,
            'tags': tags,
            'comments': comments,
            'like_count': like_count,
            'liked': liked,
            'token': token

            }
    return render(request, 'pages/recipe.html', args)



