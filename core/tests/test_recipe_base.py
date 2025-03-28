from django.test import TestCase
from core.models import Recipe, Category, User


class RecipeMixin:

    def make_category(self, name="Categoria"):
        return Category.objects.create(name=name)

    def make_author(
        self,
        username="retiano",
        email="retiano@email.com",
        password="retianosenha1234$",
        first_name="ret",
        last_name="iano",
    ):
         return User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
            )

    def make_recipe(
        self,
        category_data= None,
        author_data=None,
        title = 'Recipe title',
        description = 'Description-title',
        slug = 'recipe-slug',
        preparation_time = 10,
        preparation_time_unit = 'minutes',
        servings = 5,
        servings_unit = 'portions',
        preparation_steps = 'Recipe Preparation Steps',
        preparation_steps_is_html = False,
        is_published = True,
        ):

        if category_data is None:
            category_data = {}

        if author_data is None:
            author_data = {}
         
        return Recipe.objects.create(
            category= self.make_category(**category_data),
            author= self.make_author(**author_data),
            title = title,
            description = description,
            slug = slug,
            preparation_time = preparation_time,
            preparation_time_unit = preparation_time_unit,
            servings = servings,
            servings_unit = servings_unit,
            preparation_steps = preparation_steps,
            preparation_steps_is_html = preparation_steps_is_html,
            is_published = is_published,
            )
    
    def make_recipe_in_batch(self, qtd=5):
        recipes = []
        for i in range(qtd):
            kwargs = {
                "title" : f'Recipe Title {i}',
                "author_data" : {"username" : f'u{i}'},
                "slug" : f"Recipe-title-{i}",
            }
            recipe = self.make_recipe(**kwargs)
            recipes.append(recipe)
        return recipes

class RecipeTestBase(TestCase, RecipeMixin):

    def setUp(self):
        return super().setUp()
    
    

    