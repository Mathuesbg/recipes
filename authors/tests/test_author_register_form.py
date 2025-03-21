from unittest import TestCase
from django.test import TestCase as DjangoTestCase
from authors.forms import RegisterForm
from parameterized import parameterized
from django.urls import reverse

class AuthorRegisterFormUnitTest(TestCase):

    @parameterized.expand([
        ('username','type your username'),
        ('last_name','type your last name'),
        ('first_name','type your first name'),
        ('email','type your email'),
        ('password','type your password'),
        ('password2','confirm your password'),
    ])
    def test_fields_placeholder_is_correct(self, field, placeholder):
        form = RegisterForm()
        value = form[field].field.widget.attrs['placeholder']
        self.assertEqual(placeholder, value)

    @parameterized.expand([
        ('username',(
            'Username must have letters,'
            ' number or one of those "@ . + - _ "'
            'the length shoud be between 4 and 150 characters'
            )
        ),
        ('email','The e-mail must be valid'),
        ('password', (
            'password must have at least one uppercase letter, '
            'One lowercase letter and one number. The length should be'
            'at least 8 letters.'
            )
        ),
    ])
    def test_fields_help_text_is_correct(self, field, help_text):
        form = RegisterForm()
        current = form[field].field.help_text
        
        self.assertEqual(help_text, current)


    @parameterized.expand(
            [  
        ('username','Username'),
        ('last_name','Last name'),
        ('first_name','First name'),
        ('email','E-mail'),
        ('password','Password'),
        ('password2','Password Confirmation'),
        ]
    )  
    def test_fields_label_is_correct(self, field, label_val):
        form = RegisterForm()
        current = form[field].field.label
        
        self.assertEqual(label_val, current)


class AuthorRegisterFormIntegration(DjangoTestCase):
    def setUp(self, *args, **kwarg):
        self.form_data = {
            'username' : 'user',
            'first_name' : 'first',
            'last_name' : 'last',
            'email' : 'email@email.com',
            'password' : 'Strongpassword1',
            'password2' : 'Strongpassword1'
        }
        return super().setUp(*args, **kwarg)
    

    @parameterized.expand([
            ('username' , 'This field must not be empty'),
            ('first_name' , 'Write your first name'),
            ('last_name' , 'Write your last name'),
            ('email' , 'Write your email'),
            ('password' , 'Password can`t be empty'),
            ('password2' , 'Please repeat your password'),
    ])
    def test_fields_cannot_be_empty(self, field, msg):
        self.form_data[field] = ''
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn(msg, response.content.decode('utf-8'))

    def test_user_name_field_min_length_should_be_4(self):
        self.form_data['username'] = 'jao'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Username must have at least 4 characters"
        self.assertIn(msg, response.context['form'].errors['username'])

    def test_user_name_field_max_length_should_be_less_than_150(self):
        self.form_data['username'] = 'a' * 151
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = "Username must have less than 150 characters"
        self.assertIn(msg, response.context['form'].errors['username'])


    def test_password_field_have_lower_upper_case_letters(self):
        self.form_data['password'] = 'abc'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = (
            'Password must have at least one uppercase letter,'
            ' one lowercase letter and one number. '
            'The length should be at least 8 characters.'
            )
        self.assertIn(msg, response.context['form'].errors['password'])

        self.form_data['password'] = 'Strongpsswrd123'
        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        
        print()
        self.assertNotIn('password', response.context['form'].errors)

    def test_password_and_password_confirmation_are_equal(self):

        self.form_data['password'] = 'Strongpsswrd12'
        self.form_data['password2'] = 'Strongpsswrd123'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'passwords must be equal!'

        self.assertIn(msg, response.content.decode('utf-8'))
        self.assertIn(msg, response.context['form'].errors.get("password2"))


        self.form_data['password2'] = 'Strongpsswrd12'

        url = reverse('authors:create')
        response = self.client.post(url, data=self.form_data, follow=True)
        msg = 'passwords must be equal!'
        self.assertNotIn(msg, response.content.decode('utf-8'))


    def test_send_get_request_to_registration_create_view_returns_404(self):

        url = reverse('authors:create')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 404)


    def test_email_field_must_be_unique(self):
        
        url = reverse('authors:create')
        
        response1 = self.client.post(url, data=self.form_data, follow=True)
        self.assertIn("Author registered successfully!", response1.content.decode('utf-8'))

        response2 = self.client.post(url, data=self.form_data, follow=True)
        msg = 'This email is already registered'

        self.assertIn(msg, response2.context['form'].errors['email'])
        self.assertIn( msg, response2.content.decode('utf-8'))

