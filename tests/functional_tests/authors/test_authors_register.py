from .base import AuthorsBaseTest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pytest


@pytest.mark.functional_test
class AuthorsRegisterTest(AuthorsBaseTest):
    
    def get_form(self):
        return self.browser.find_element(
            By.XPATH,
            "/html/body/main/div[2]/form"  
        )
    
    def fill_form_dummy_data(self, form):

        fields = form.find_elements(By.TAG_NAME, 'input')

        for field in fields:
            if field.is_displayed():
                field.send_keys(' ' * 20)

    def form_field_test_with_callback(self, callback):
        self.browser.get(self.live_server_url + '/authors/register/')
        form = self.get_form()

        self.fill_form_dummy_data(form)

        email = form.find_element(By.NAME, 'email')
        email.send_keys('dummy@email.com')

        callback(form)

        return form

    def test_empty_first_name_error_message(self):
        
        def callback(form):
            first_name_field = self.get_by_placeholder(form, "type your first name")
            first_name_field.send_keys(' ')
            first_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your first name', form.text)

        self.form_field_test_with_callback(callback)

    def test_empty_last_name_error_message(self):
        
        def callback(form):
            last_name_field = self.get_by_placeholder(form, "type your last name")
            last_name_field.send_keys(' ')
            last_name_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn('Write your last name', form.text)

        self.form_field_test_with_callback(callback)


    def test_empty_username_error_message(self):
        
        def callback(form):
            username_field = self.get_by_placeholder(form, "type your username")
            username_field.send_keys(' ')
            username_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn(
                'This field must not be empty',
                form.text
            )

        self.form_field_test_with_callback(callback)

    def teste_invalid_email_error_message(self):
        
        def callback(form):
            email_field = self.get_by_placeholder(form, "type your email")
            email_field.send_keys('email@invalid')
            email_field.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn(
                'The e-mail must be valid',
                form.text
            )
        self.form_field_test_with_callback(callback)

    def teste_passwords_dont_match(self):
        
        def callback(form):

            password1 = self.get_by_placeholder(form, "type your password")
            password1.send_keys('@Bc12345')

            password2 = self.get_by_placeholder(form, "confirm your password")
            password2.send_keys('@Bc12346')

            password2.send_keys(Keys.ENTER)

            form = self.get_form()

            self.assertIn(
                'passwords must be equal!',
                form.text
            )
        self.form_field_test_with_callback(callback)

    def test_user_valid_data_register_successfully(self):

        self.browser.get(self.live_server_url + "/authors/register/")
        form = self.get_form()

        self.get_by_placeholder(form, "type your first name").send_keys('First Name')
        self.get_by_placeholder(form, "type your last name").send_keys('Last Name')
        self.get_by_placeholder(form, "type your username").send_keys('Username')
        self.get_by_placeholder(form, "type your email").send_keys('email@email.com')
        self.get_by_placeholder(form, "type your password").send_keys('@Bc12345')
        ent = self.get_by_placeholder(form, "confirm your password")
        ent.send_keys('@Bc12345')
        ent.send_keys(Keys.ENTER)


        self.assertIn(
            "Author registered successfully!",
            self.browser.find_element(by=By.TAG_NAME, value='body').text
        )
