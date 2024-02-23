from django.contrib import admin
from django.urls import path

from words import views

urlpatterns = [
    path('', views.Words.as_view(), name='all_words'),
    path('<int:word_id>/', views.word, name='word'),
    path('random/', views.random_word, name='random_word'),
]
