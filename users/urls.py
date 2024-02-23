from django.contrib import admin
from django.urls import path

from users import views

urlpatterns = [
    path('login/', views.login_handler, name='login'),
    path('logout/', views.logout_handler, name='logout'),
    path('register/', views.register_handler, name='register'),
    path('user/', views.user_handler, name='user'),
    path('user/delete/', views.user_delete_handler, name='user_delete'),
    path('leaderboard/', views.leaderboard, name='leaderboard'),
]
