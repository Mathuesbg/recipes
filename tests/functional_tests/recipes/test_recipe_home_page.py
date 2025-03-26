from selenium.webdriver.common.by import By
import pytest
from .base import RecipeBaseFunctionalTest
from time import sleep


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_returns_recipes_not_found(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body')
        self.assertIn("No recipes found here", body.text)
