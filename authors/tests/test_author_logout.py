from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class AuthorLogoutTest(TestCase):
    

    def test_user_tries_to_logout_using_get_method(self):
        
        User.objects.create_user(username='Pedrinhow', password="@Bc12345")
        self.client.login(username='Pedrinhow', password="@Bc12345")

        url = reverse("authors:logout")
        response = self.client.get(url, follow=True)
        
        self.assertIn(f'invalid logout request', response.content.decode("utf-8"))

    
    def test_user_tries_to_logout_using_another_user(self):
        
        User.objects.create_user(username='Pedrinhow', password="@Bc12345")
        self.client.login(username='Pedrinhow', password="@Bc12345")

        url = reverse("authors:logout")
        response = self.client.post(url, data={"username" : "another_user"} ,follow=True)
        
        self.assertIn(f'invalid logout user', response.content.decode("utf-8"))

    def test_user_logout_successfully(self):
        
        User.objects.create_user(username='Pedrinhow', password="@Bc12345")
        self.client.login(username='Pedrinhow', password="@Bc12345")

        url = reverse("authors:logout")
        response = self.client.post(url, data={"username" : "Pedrinhow"} ,follow=True)
        
        self.assertIn(f'logout successfully!', response.content.decode("utf-8"))