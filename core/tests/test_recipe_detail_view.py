from django.urls import reverse, resolve
from core import views
from core.tests.test_recipe_base import RecipeTestBase


class RecipeDetailViewTest(RecipeTestBase):

    def test_recipe_detail_view_function_is_correct(self):
        view = resolve(reverse('recipe:recipe', kwargs={'id':1}))
        self.assertIs(view.func, views.recipe)

    def test_recipe_detail_view_returns_404_if_no_recipe_found(self):
        response = self.client.get(reverse('recipe:recipe', kwargs={'id':1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_detail_template_loads_recipes(self):

        recipe = self.make_recipe(title='this is a detail test')

        response = self.client.get(reverse('recipe:recipe', args=(recipe.id,)))
        response_content = response.content.decode('utf-8')

        self.assertIn( 'this is a detail test', response_content)

    def test_recipe_detail_template_doesnt_load_unpublished_recipe(self):

        recipe = self.make_recipe(is_published=False)

        response = self.client.get(reverse('recipe:recipe', args=(recipe.id,)))

        self.assertEqual(response.status_code, 404)
