from django.test import TestCase
from django.urls import reverse, resolve
from core import views


class RecipeViewsTest(TestCase):
    
    # HOME

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

    # ENDHOME

    # CATEGORY
    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipe:category', kwargs={'category_id':1}))
        self.assertIs(view.func, views.category)
    
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipe:category', kwargs={'category_id':1000}))
        self.assertEqual(response.status_code, 404)
        
    # ENDCATEGORY

    # DETAIL
    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipe:recipe', kwargs={'id':1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipe:recipe', kwargs={'id':1000}))
        self.assertEqual(response.status_code, 404)
    # ENDDETAIL