from django.shortcuts import render
from account.views import userDetails
from recipe.models import Recipe, Ingredient, Nutrients


def recipe(request, recipe_id):
    uDetails = userDetails(request)
    recipeDetails = Recipe.objects.get(id=recipe_id)
    ingredients = Ingredient.objects.filter(recipe_id=recipe_id)
    nutrients = Nutrients.objects.filter(recipe_id=recipe_id, entry_type='totalNutrients' )

    args = {'title': "Recipe",
            'left_menu_selected': '',
            'is_auth': uDetails['is_auth'],
            'user_name': uDetails['user_name'],
            'profile_photo': uDetails['profile_photo'],
            'recipe_id': recipe_id,
            'recipe_name': recipeDetails.recipe_name,
            'recipe_description': recipeDetails.recipe_description,
            'recipe_category': recipeDetails.recipe_category,
            'recipe_cuisine': recipeDetails.recipe_cuisine,
            'recipe_added_date': recipeDetails.added_date,
            'recipe_how_many_person': recipeDetails.how_many_person,
            'calories_total': recipeDetails.calories_total,
            'healthLabels': recipeDetails.healthLabels,
            'cautions': recipeDetails.cautions,
            'ingredients': ingredients,
            'nutrients': nutrients,
            'my_recipe_count': uDetails['recipe_count'],
            'my_notification_count': uDetails['notification_count']
            }
    return render(request, 'pages/recipe.html', args)



