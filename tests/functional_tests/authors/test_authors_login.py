from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from django.urls import reverse
from time import sleep
import pytest


@pytest.mark.functional_test
class AuthorsLoginTest(AuthorsBaseTest):

    def test_user_valid_data_can_login_successfully(self):
        user = User.objects.create_user(username='my_user', password='@Bc12345')

        url = reverse("authors:login")
        self.browser.get(self.live_server_url + url)
        form = self.browser.find_element(By.CLASS_NAME, "main-form")

        field_username = self.get_by_placeholder(form, 'Type your username here')
        field_username.send_keys(user.username)
        
        field_password = self.get_by_placeholder(form, 'Type your password here')
        field_password.send_keys('@Bc12345')

        form.submit()

        self.assertIn(
            f'You are logged in with "{user.username}".', 
            self.browser.find_element(By.TAG_NAME, "body").text
            )


    def test_login_create_raises_404_if_not_POST_method(self):
        url = reverse("authors:login_create")
        self.browser.get(self.live_server_url + url)

        self.assertIn(
            "Not Found",
            self.browser.find_element(By.TAG_NAME, "body").text
        )
        

    def teste_form_login_is_invalid(self):
        self.browser.get(
            self.live_server_url + reverse("authors:login")
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Type your username here')
        password = self.get_by_placeholder(form, 'Type your password here')

        username.send_keys(' ')
        password.send_keys(" ")

        form.submit()
        self.assertIn("Form error!", self.browser.find_element(By.TAG_NAME, "body").text)


    def teste_form_login_is_invalid_credentials(self):
        self.browser.get(
            self.live_server_url + reverse("authors:login")
        )

        form = self.browser.find_element(By.CLASS_NAME, 'main-form')

        username = self.get_by_placeholder(form, 'Type your username here')
        password = self.get_by_placeholder(form, 'Type your password here')

        username.send_keys('invald_user')
        password.send_keys("invalid_@Bc12345")

        form.submit()
        self.assertIn("invalid credentials", self.browser.find_element(By.TAG_NAME, "body").text)