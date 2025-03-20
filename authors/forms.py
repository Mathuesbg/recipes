import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError(
            message=(
            'Password must have at least one uppercase letter, '
            'one lowercase letter and one number. The length should be '
            'at least 8 characters.'
            ),
            code='invalid'
        )

def add_attr(field, attr_name, new_attr_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing}{new_attr_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val )


class RegisterForm(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'type your username')
        add_placeholder(self.fields['last_name'], 'type your last name')
        add_placeholder(self.fields['first_name'], 'type your first name')
        add_placeholder(self.fields['email'], 'type your email')
        add_placeholder(self.fields['password'], 'type your password ')
        add_placeholder(self.fields['password2'], 'confirm your password')

    password = forms.CharField(
        required=True,
        widget= forms.PasswordInput(),
        error_messages = {
            'required' : 'Password can`t be empty'
        },
        help_text= (
            'password must have at least one uppercase letter, '
            'One lowercase letter and one number. The length should be'
            'at least 8 letters.'
        ),
        validators=[strong_password],
        label= "Password"
    )

    password2 = forms.CharField(
        required=True,
        widget= forms.PasswordInput(),
        label= 'Password Confirmation'
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password',
        ]

        labels = {
            'first_name' : "First name",
            'username' : "Username",
            'last_name' : "Last name",
            'email' : "E-mail", 
        }

        help_texts = {
            'email' : 'The e-mail must be valid'
        }

        error_messages = { 
            "username": {
                "required" : 'This field must not be empty',
            }
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError(
                {'password2' : 'passwords must be equal!'}
                
            )
