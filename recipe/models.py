from django.db import models
from account.models import Account
from foodproviders.models import FoodProviders

# Cuisines are just like categories with basic structure.
# Every recipe has a cuisine
class Cuisine(models.Model):
    cuisine_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cuisine_name

# Every recipe has a category
class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name

# Only Food Providers can add menu
# Food providers can add recipes to a menus
class Menus(models.Model):
    menu_name = models.CharField(max_length=100)
    menu_provider = models.ForeignKey(FoodProviders, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.menu_name

# Recipe model consist of name, description, cuisine, category and person count
# Users can create recipe for their food providers -> recipe_food_provider
class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    recipe_user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_food_provider = models.ForeignKey(FoodProviders, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_description = models.TextField(blank=True)
    recipe_cuisine = models.ForeignKey(Cuisine, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    how_many_person = models.IntegerField()
    added_date = models.DateTimeField()

    def __str__(self):
        return self.recipe_name + " -> " + self.recipe_user.username


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=300)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.ingredient_name

# nutrients are in relation with only recipe itself. Not ingredients.
class Nutrients(models.Model):

    nutrient_name = models.CharField(max_length=200)
    nutrient_quantity = models.FloatField(default=0.0)
    nutrient_unit = models.CharField(max_length=300)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.nutrient_name


class Tags(models.Model):
    tag_name = models.CharField(max_length=200)
    tag_tid = models.CharField(max_length=200)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.tag_name

# relation beetween recipe and menu
class Menu_Recipe(models.Model):
    menu_id = models.ForeignKey(Menus, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.menu_id.menu_name + " -> " + self.recipe_id.recipe_name


class Comments(models.Model):
    comment = models.CharField(max_length=600)
    comment_user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField()

    def __str__(self):
        return self.comment


class Likes(models.Model):
    like_user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField()

    def __str__(self):
        return self.like_user.username

# daily nutrients are already added to database
# system uses this model to compare recipe nutrient values and added values for daily needs
class Daily_Nutrients(models.Model):
    nutrient_name = models.CharField(max_length=200)
    nutrient_unit = models.CharField(max_length=300)
    needed = models.FloatField(default=0.0)
    gender_role = (('Female', "Female"), ('Male', "Male"))
    gender = models.CharField(max_length=10, choices=gender_role, verbose_name='gender', default='Female')
    age = models.IntegerField(default=20)

    def __str__(self):
        return self.nutrient_name + " ... " + str(self.needed) + self.nutrient_unit + "... " + self.gender + "-" + str(self.age)