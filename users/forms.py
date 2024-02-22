from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.forms import ModelForm


class RegisterUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        help_texts = {
            'username': None,
            'email': None,
            'password': None,
        }