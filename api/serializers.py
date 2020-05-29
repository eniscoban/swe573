from recipe.models import Recipe
from rest_framework import serializers


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'recipe_name', 'recipe_description', 'recipe_user', 'recipe_cuisine', 'recipe_category')
