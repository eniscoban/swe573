from django.contrib import admin
from recipe.models import Recipe, Category, Cuisine, Ingredient, Nutrients

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Cuisine)
admin.site.register(Ingredient)
admin.site.register(Nutrients)