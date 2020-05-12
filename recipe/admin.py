from django.contrib import admin
from recipe.models import Recipe, Category, Cuisine, Ingredient, Nutrients

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Cuisine)
admin.site.register(Ingredient)


class NutrientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'nutrient_name', 'recipe_id', 'entry_type']

admin.site.register(Nutrients, NutrientsAdmin)