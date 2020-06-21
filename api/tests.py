from django.test import TestCase
import json
from django.contrib.auth.models import User
from account.models import Account, Follower
from django.urls import reverse
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from api.serializers import RecipeSerializer
from recipe.models import Recipe, Cuisine, Category, Ingredient, Nutrients, Tags, Comments, Likes
from django.utils.timezone import now
from django.core import serializers



class TestApi(APITestCase):

    def setUp(self):
        self.user = Account.objects.create_user(email="test@test.com", username="test1", password="13456782")
        self.user2 = Account.objects.create_user(email="test2@test2.com", username="test2", password="13456782")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + str(self.token))


    def test_create_recipe(self):

        tags = [{'tid': 'tag1', 'name':'tag1'}, {'tid': 'tag2', 'name': 'tag2'}]
        serialized_tags = json.dumps(tags)

        ingredients = [{'name': 'name1', 'fdcId': 'fdcId1'}, {'name': 'name2', 'fdcId': 'fdcId2'}]
        serialized_ingredients = json.dumps(ingredients)

        nutrients = [
            {'nutrient_name': 'nutrient_name1', 'nutrient_unit': 'nutrient_unit1', 'nutrient_amount':500, 'ingredient_id':1},
            {'nutrient_name': 'nutrient_name2', 'nutrient_unit': 'nutrient_unit2', 'nutrient_amount':400, 'ingredient_id':1},
            {'nutrient_name': 'nutrient_name3', 'nutrient_unit': 'nutrient_unit3', 'nutrient_amount':300, 'ingredient_id':1}
        ]
        serialized_nutrients = json.dumps(nutrients)


        cui = Cuisine.objects.create(cuisine_name="cuisine")
        cat = Category.objects.create(category_name="category")

        data = {
            "recipe_name": "recipe_name",
            "recipe_description": "recipe_description",
            "recipe_category": cat.id,
            "recipe_cuisine": cui.id,
            "recipe_serving": 3,
            "user_select": 0,
            "tags": serialized_tags,
            "ingredients": serialized_ingredients,
            'nutrients': serialized_nutrients
        }

        response = self.client.post("/api/create_recipe/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_follow_user(self):
        data = {
            'target_username': "test2"
        }
        response = self.client.post("/api/follow_user/", data)
        u = Follower.objects.get(target=self.user2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(u.follower, self.user)


    def test_like_recipe(self):
        self.recipe1 = Recipe.objects.create(
            recipe_name="test Recipe",
            recipe_user=self.user,
            recipe_description='test',
            how_many_person=2,
            added_date=now()
        )
        data = {
            "recipe_id": self.recipe1.id
        }
        response = self.client.post("/api/like_recipe/", data)
        like_count = Likes.objects.all().count()
        like_user = Likes.objects.get(recipe_id=self.recipe1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(like_count, 1)
        self.assertEquals(like_user.like_user, self.user)

    def test_comment_recipe(self):
        self.recipe1 = Recipe.objects.create(
            recipe_name="test Recipe",
            recipe_user=self.user,
            recipe_description='test',
            how_many_person=2,
            added_date=now()
        )
        data = {
            'comment': "test comment",
            'recipe_id': self.recipe1.id
        }
        response = self.client.post("/api/add_comment/", data)
        comment_count = Comments.objects.all().count()
        comment_user = Comments.objects.get(recipe_id=self.recipe1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEquals(comment_count, 1)
        self.assertEquals(comment_user.comment_user, self.user)
