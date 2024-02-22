from django.contrib.auth.models import User
from django.db import models
from django.db.models import ForeignKey, CharField


# Create your models here.

class UserDict(models.Model):
    user = ForeignKey(User, on_delete=models.CASCADE, editable=False)
    word = CharField(max_length=50)
    translation = CharField(max_length=50)
    transcription = CharField(max_length=50)
    transliteration = CharField(max_length=50)
    audio = CharField(max_length=255)
