from django.test import TestCase, Client

from django.urls import reverse
from account.models import Account
from recipe.models import Recipe, Cuisine, Category, Ingredient, Nutrients, Tags, Comments, Likes
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()
        self.my_recipes_url = reverse('my_recipes')
        self.create_recipe_url = reverse('create_recipe_page')

        self.user = Account.objects.create_user('eniscoban@gmail.com', 'eniscoban', '1q2w3e4r')
        self.client.login(email='eniscoban@gmail.com', password='1q2w3e4r')

        self.cui = Cuisine.objects.create(cuisine_name='test_name')
        self.cuisine_url = reverse('cuisine', args=[self.cui.id])

    def test_my_recipes(self):

        response = self.client.get(self.my_recipes_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/my_recipes.html')

    def test_create_recipe(self):

        response = self.client.get(self.create_recipe_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/create_recipe.html')

    def test_cuisine(self):
        response = self.client.get(self.cuisine_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'pages/cuisine.html')
