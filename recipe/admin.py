from django.contrib import admin
from recipe.models import Recipe, Category, Cuisine, Ingredient, Nutrients, Tags, Comments

admin.site.register(Recipe)
admin.site.register(Category)
admin.site.register(Cuisine)
admin.site.register(Ingredient)
admin.site.register(Tags)
admin.site.register(Comments)


class NutrientsAdmin(admin.ModelAdmin):
    list_display = ['id', 'nutrient_name', 'nutrient_quantity', 'nutrient_unit']

admin.site.register(Nutrients, NutrientsAdmin)