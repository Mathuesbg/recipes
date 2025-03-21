from django.urls import reverse, resolve
from core import views
from core.tests.test_recipe_base import RecipeTestBase
from unittest.mock import patch

class RecipeHomeViewTest(RecipeTestBase):

    def test_recipe_home_view_function_is_correct(self):
            view = resolve(reverse('recipe:home'))
            self.assertIs(view.func, views.home)

    def test_recipe_home_view_returns_200_ok(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertEqual(response.status_code, 200)
    
    def test_recipe_home_view_loads_correctly_template(self):
        response = self.client.get(reverse('recipe:home'))
        self.assertTemplateUsed(response=response, template_name="core/pages/home.html")


    def test_recipe_home_template_shows_no_recipe_founds_if_no_recipes(self):
        
        response = self.client.get(reverse('recipe:home'))
        self.assertIn(
            "No recipes found here",
            response.content.decode("utf-8")
            )
        
    def test_recipe_home_template_loads_recipes(self):
        self.make_recipe()
        response = self.client.get(reverse('recipe:home'))
        response_content = response.content.decode('utf-8')
        response_context = response.context.get("recipes")

        self.assertEqual(len(response_context), 1)
        self.assertIn( "Description-title", response_content)


    def test_recipe_home_template_doesnt_load_unpublished_recipes(self):

        self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipe:home'))
        response_context = response.context.get("recipes")

        self.assertEqual(len(response_context), 0)


    @patch("core.views.PER_PAGE", new=2)
    def test_recipe_home_is_paginated(self):

        for i in range(3):
            kwargs = {
                "author_data" : {"username" : f'u{i}'},
                "slug" : f"r{i}",
            }
            self.make_recipe(**kwargs)

        response = self.client.get(reverse('recipe:home'))
        recipes = response.context.get("recipes")
        paginator = recipes.paginator
       

        self.assertEqual(paginator.num_pages, 2)
        self.assertEqual(len(paginator.get_page(1)), 2)


    @patch("core.views.PER_PAGE", new=2)
    def test_invalid_page_query_uses_page_1(self):
        for i in range(3):
            kwargs = {
                "author_data" : {"username" : f'u{i}'},
                "slug" : f"r{i}",
            }
            self.make_recipe(**kwargs)


        response = self.client.get(reverse('recipe:home') + "?page=1a")

        self.assertEqual(response.context.get("recipes").number, 1)

        response = self.client.get(reverse('recipe:home') + "?page=2a")

        self.assertEqual(response.context.get("recipes").number, 1)