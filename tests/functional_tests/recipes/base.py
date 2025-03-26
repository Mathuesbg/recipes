from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from utils.browser import make_chrome_browser
from core.tests.test_recipe_base import RecipeMixin


class RecipeBaseFunctionalTest(StaticLiveServerTestCase, RecipeMixin):
    def setUp(self):
        self.browser = make_chrome_browser()
        return super().setUp()
    
    def tearDown(self):
        self.browser.quit()
        return super().tearDown()

