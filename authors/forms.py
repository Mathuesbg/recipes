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
        add_placeholder(self.fields['username'], 'type your username here')
        add_placeholder(self.fields['last_name'], 'type your last name here')
        add_placeholder(self.fields['first_name'], 'type your first name here')
        add_placeholder(self.fields['email'], 'type your email here')

    password = forms.CharField(
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder' : "type your password",
            }
        ),
        error_messages = {
            'required' : 'Password can`t be empty'
        },
        help_text= (
            'password must have at least one uppercase letter, '
            'One lowercase letter and one number. The length should be'
            'at least 8 letters.'
        ),
        validators=[strong_password]
    )

    password2 = forms.CharField(
        required=True,
        widget= forms.PasswordInput(
            attrs={
                'placeholder' : "confirm your password",
            }
        ),
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
            'username' : "User name",
            'last_name' : "Last name",
            'email' : "E-mail",
            'password' : "Password"
        }

        help_texts = {
            'email' : 'The e-mail must be valid'
        }

        error_messages = { 
            "username": {
                "required" : 'This field must not be empty',
            }
        }

        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder' : "type your name here"
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder' : "type your password here"
            })
        }
    
    def clean_password(self):
        data = self.cleaned_data.get('password')
        if 'atencao' in data:
            raise ValidationError(
                message='password can`t contain the "atention" word!',
                code='invalid',
                params={'values':'atencao'}
            )
        return data
    
    def clean_first_name(self):
        data = self.cleaned_data.get('first_name')
        if 'John Doe' in data:
            raise ValidationError(
                message='password can`t contain the %(values)s name!',
                code='invalid',
                params={'values':'John Doe'}
            )
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError(
                {'password2' : 'passwords must be equal!'}
                
            )
