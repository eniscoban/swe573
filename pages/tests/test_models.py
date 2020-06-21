from django.test import TestCase, Client
from rest_framework.test import APIClient

csrf_client = Client(enforce_csrf_checks=True)


from recipe.models import Recipe, Cuisine, Category, Ingredient, Nutrients, Tags, Comments, Likes
from account.models import Account
from django.utils.timezone import now
from rest_framework.authtoken.models import Token

class TestModels(TestCase):

    def setUp(self):
        self.user = Account.objects.create_user('eniscoban@gmail.com', 'eniscoban', '1q2w3e4r')
        self.client.login(email='eniscoban@gmail.com', password='1q2w3e4r')



        self.token, _ = Token.objects.get_or_create(user=self.user)

        self.recipe1 = Recipe.objects.create(
            recipe_name="test Recipe",
            recipe_user=self.user,
            recipe_description='test',
            how_many_person=2,
            added_date=now()

        )

    def test_ingredient_count(self):
        Ingredient.objects.create(ingredient_name="ingredient1", recipe_id=self.recipe1)
        Ingredient.objects.create(ingredient_name="ingredient2", recipe_id=self.recipe1)
        countIng = Ingredient.objects.all().count()
        self.assertEquals(countIng, 2)

    def test_nutrient_count(self):
        Nutrients.objects.create(nutrient_name="nutrient1",nutrient_quantity=100, nutrient_unit="gr", recipe_id=self.recipe1)
        Nutrients.objects.create(nutrient_name="nutrient2",nutrient_quantity=200, nutrient_unit="gr", recipe_id=self.recipe1)
        Nutrients.objects.create(nutrient_name="nutrient3",nutrient_quantity=300, nutrient_unit="gr", recipe_id=self.recipe1)
        countIng = Nutrients.objects.all().count()
        self.assertEquals(countIng, 3)

    def test_like(self):
        Likes.objects.create(like_user=self.user,
                             recipe_id=self.recipe1,
                             added_date=now()
                             )
        like_count = Likes.objects.all().count()
        self.assertEquals(like_count, 1)