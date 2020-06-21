from django.test import SimpleTestCase
from django.urls import reverse, resolve
from pages.views import home, my_recipes, cuisine, category, tag, create_recipe


class TestUrls(SimpleTestCase):

    def test_home_url_is_resolved(self):
        url = reverse('home')
        print(resolve(url))
        self.assertEquals(resolve(url).func, home)

    def test_my_recipes_url_is_resolved(self):
        url = reverse('my_recipes')
        print(resolve(url))
        self.assertEquals(resolve(url).func, my_recipes)

    def test_cuisine_url_is_resolved(self):
        url = reverse('cuisine', args=['some_cuisine'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, cuisine)

    def test_category_url_is_resolved(self):
        url = reverse('category', args=['some_category'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, category)

    def test_tag_url_is_resolved(self):
        url = reverse('tag', args=['tag'])
        print(resolve(url))
        self.assertEquals(resolve(url).func, tag)

    def test_create_recipe_url_is_resolved(self):
        url = reverse('create_recipe_page')
        self.assertEquals(resolve(url).func, create_recipe)



