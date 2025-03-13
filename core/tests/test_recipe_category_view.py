from django.urls import reverse, resolve
from core import views
from core.tests.test_recipe_base import RecipeTestBase


class RecipeCategoryViewTest(RecipeTestBase):

    def test_recipe_category_view_function_is_correct(self):
        view = resolve(reverse('recipe:category', kwargs={'category_id':1}))
        self.assertIs(view.func, views.category)
    
    def test_recipe_category_view_returns_404_if_no_recipes_found(self):
        response = self.client.get(reverse('recipe:category', kwargs={'category_id':1000}))
        self.assertEqual(response.status_code, 404)

    def test_recipe_category_template_loads_recipes(self):

        recipe = self.make_recipe(title='this is a category test')

        response = self.client.get(reverse('recipe:category', args=(recipe.category.id,)))
        response_content = response.content.decode('utf-8')

        self.assertIn( 'this is a category test', response_content)

    def test_recipe_category_template_doesnt_load_unpublished_recipes(self):

        recipe = self.make_recipe(is_published=False)
        response = self.client.get(reverse('recipe:category', args=(recipe.category.id,)))

        self.assertEqual(response.status_code, 404)