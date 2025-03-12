from django.test import TestCase
from django.urls import reverse


class RecipeURLsTest(TestCase):

    def test_recipe_home_url_is_correct(self):
        url = reverse("recipe:home")
        self.assertEqual(url, '/')

    def test_recipe_category_url_is_correct(self):
        url = reverse("recipe:category", kwargs={'category_id':1})
        self.assertEqual(url, '/recipe/category/1/')

    def test_recipe_detail_url_is_correct(self):
        url = reverse("recipe:recipe", kwargs={'id':1})
        self.assertEqual(url, '/recipe/1/')

    def test_recipe_search_url_is__correct(self):
        url = reverse("recipe:search")
        self.assertEqual(url, '/recipe/search/')