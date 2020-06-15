from django.contrib import admin
from recipe.models import Recipe, Category, Cuisine, Ingredient, Nutrients, Tags, Comments, Likes

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Cuisine)
admin.site.register(Ingredient)
admin.site.register(Tags)
admin.site.register(Comments)
admin.site.register(Likes)


class NutrientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'nutrient_name', 'nutrient_quantity', 'nutrient_unit']

admin.site.register(Nutrients, NutrientsAdmin)