from django.test import TestCase
from authors.forms import RegisterForm
from parameterized import parameterized

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
            'Obrigatório. 150 caracteres ou menos. '
            'Letras, números e @/./+/-/_ apenas.'
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
        print("oi")
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
        print("oi")
        self.assertEqual(label_val, current)