from core.tests.test_recipe_base import RecipeTestBase
from django.core.exceptions import ValidationError


class RecipeCategoryModelTest(RecipeTestBase):
    def setUp(self):
        self.category = self.make_category()
        return super().setUp()
    
    def test_category_string_representation(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_recipe_category_model_name_max_length_is_65_chars(self):
        self.category.name = 'A' * 66
        with self.assertRaises(ValidationError):
            self.category.full_clean()