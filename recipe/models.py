from django.db import models
from account.models import Account

class Cuisine(models.Model):
    cuisine_name = models.CharField(max_length=100)

    def __str__(self):
        return self.cuisine_name


class Category(models.Model):
    category_name = models.CharField(max_length=100)

    def __str__(self):
        return self.category_name


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=200)
    recipe_user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_description = models.TextField(blank=True)
    recipe_cuisine = models.ForeignKey(Cuisine, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    yield_total = models.CharField(max_length=100, default="")
    calories_total = models.FloatField(default=0.0)
    weight_total = models.FloatField(default=0.0)
    healthLabels = models.CharField(max_length=300, default="")
    cautions = models.CharField(max_length=300, default="")

    how_many_person = models.IntegerField()
    added_date = models.DateTimeField()

    def __str__(self):
        return self.recipe_name


class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=300)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.ingredient_name


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


class Comments(models.Model):
    comment = models.CharField(max_length=600)
    comment_user = models.ForeignKey(Account, null=True, blank=True, on_delete=models.SET_NULL)
    recipe_id = models.ForeignKey(Recipe, null=True, blank=True, on_delete=models.SET_NULL)
    added_date = models.DateTimeField()

    def __str__(self):
        return self.comment
