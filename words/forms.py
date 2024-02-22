from django.forms import ModelForm
from words.models import UserDict


class PartialWordForm(ModelForm):
    class Meta:
        model = UserDict
        exclude = ['user']
