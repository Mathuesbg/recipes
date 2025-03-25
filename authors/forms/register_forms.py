from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from utils.django_forms import add_placeholder, strong_password

class RegisterForm(forms.ModelForm):

    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'type your username')
        add_placeholder(self.fields['last_name'], 'type your last name')
        add_placeholder(self.fields['first_name'], 'type your first name')
        add_placeholder(self.fields['email'], 'type your email')
        add_placeholder(self.fields['password'], 'type your password ')
        add_placeholder(self.fields['password2'], 'confirm your password')


    username = forms.CharField(
        error_messages = {
            'required' : "This field must not be empty",
            'min_length' : "Username must have at least 4 characters",
            'max_length' : "Username must have less than 150 characters"
            },
        label = 'Username',
        min_length=4,
        max_length=150,

        help_text= (
            'Username must have letters,'
            ' number or one of those "@ . + - _ "'
            'the length shoud be between 4 and 150 characters'
        )
    )

    first_name = forms.CharField(
        error_messages={'required' : 'Write your first name'},
        label= 'First name'
    )

    email = forms.EmailField(
        error_messages= {'required' : 'Write your email'},
        label= 'E-mail',
        help_text = 'The e-mail must be valid'
    )

    last_name = forms.CharField(
        error_messages = {'required' : 'Write your last name'},
        label = 'Last name'
    )


    password = forms.CharField(
        widget = forms.PasswordInput(),
        error_messages = {'required' : 'Password can`t be empty'}, 
        validators = [strong_password],
        label = "Password",
        help_text = (
            'password must have at least one uppercase letter, '
            'One lowercase letter and one number. The length should be'
            'at least 8 letters.'
        ),
    )

    password2 = forms.CharField(
        widget= forms.PasswordInput(),
        label= 'Password Confirmation',
        error_messages = {'required' : 'Please repeat your password'}
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


    def clean_email(self):
        email = self.cleaned_data.get('email')
        email_exists = User.objects.filter(email=email).exists()

        if email_exists:
            raise ValidationError(
                message = 'This email is already registered', 
                code = "invalid"
                )

        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise ValidationError(
                {'password2' : 'passwords must be equal!'}
            )
