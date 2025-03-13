from django.urls import reverse, resolve
from core import views
from core.tests.test_recipe_base import RecipeTestBase


class RecipeSearchViewTest(RecipeTestBase):

    def test_recipe_search_view_function_is_correct(self):
        view = resolve(reverse('recipe:search'))
        self.assertIs(view.func, views.search)

    def test_recipe_search_loads_correct_template(self):
        url = reverse("recipe:search") + '?q=value'
        response = self.client.get(url)
        self.assertTemplateUsed(response=response,template_name='core/pages/search.html')

    def test_recipe_search_reaises_404_if_no_search_term(self):
        url = reverse("recipe:search")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_recipe_search_term_is_on_title_and_escaped(self):
        url = reverse("recipe:search") + '?q=<value>'
        response = self.client.get(url)
        template = response.content.decode("utf-8")
        self.assertIn('&quot;&lt;value&gt;&quot', template)

    def test_recipe_search_can_find_recipe_by_title(self):
        title1 = 'This is recipe one'
        title2 = 'This is recipe two'

        recipe1 = self.make_recipe(
            slug='one', title=title1, author_data={'username': 'one'}
        )
        recipe2 = self.make_recipe(
            slug='two', title=title2, author_data={'username': 'two'}
        )

        search_url = reverse('recipe:search')
        response1 = self.client.get(f'{search_url}?q={title1}')
        response2 = self.client.get(f'{search_url}?q={title2}')
        response_both = self.client.get(f'{search_url}?q=this')

        self.assertIn(recipe1, response1.context['recipes'])
        self.assertNotIn(recipe2, response1.context['recipes'])

        self.assertIn(recipe2, response2.context['recipes'])
        self.assertNotIn(recipe1, response2.context['recipes'])

        self.assertIn(recipe1, response_both.context['recipes'])
        self.assertIn(recipe2, response_both.context['recipes'])