from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest
from .base import RecipeBaseFunctionalTest
from time import sleep
from unittest.mock import patch


@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):

    def test_recipe_home_page_returns_recipes_not_found(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(by=By.TAG_NAME, value='body') 
        self.assertIn("No recipes found here", body.text)

    @patch('core.views.PER_PAGE', 2)
    def test_recipe_search_input_can_find_correct_recipes(self):

        recipes = self.make_recipe_in_batch(1)

        title_needed = "bolo de requeijao"
        recipes[0].title = title_needed
        recipes[0].save()

        self.browser.get(self.live_server_url)

        search_input = self.browser.find_element(
            by=By.XPATH, 
            value='//input[@placeholder="Search for a recipe"]')

        
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        sleep(0.1)
        container = self.browser.find_element(
            by=By.CLASS_NAME, 
            value="main-content-list").text
        
        self.assertIn(
            member=title_needed,
            container=container
            
        )


    @patch('core.views.PER_PAGE', 2)
    def test_recipe_home_page_pagination(self):
        recipes = self.make_recipe_in_batch(10)
        self.browser.get(self.live_server_url)

        page2= self.browser.find_element(
            By.XPATH,
            "//a[@aria-label='Go to page 2']"
        )

        page2.click()
        self.assertEqual(
            len(
                self.browser.find_elements(
                    by=By.CLASS_NAME, 
                    value="recipe"
                )
            ), 2
        )

