from recipe.models import Recipe
from foodproviders.models import FoodProviders
from rest_framework import serializers

# Serialize recipe model
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'recipe_name', 'recipe_description', 'recipe_user', 'recipe_cuisine', 'recipe_category')

# Serialize food provider model
class FoodProvidersSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodProviders
        fields = ('id', 'provider_name', 'provider_description', 'provider_user',
                  'provider_address', 'provider_lat', 'provider_long')
