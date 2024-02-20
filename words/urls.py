from django.contrib import admin
from django.urls import path

from words import views

urlpatterns = [
    path('', views.Words.as_view(), name='all_words'),
    path('<word_id>', views.specific_word, name='specific_word'),
]
