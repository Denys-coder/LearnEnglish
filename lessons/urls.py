from django.urls import path

from lessons import views

urlpatterns = [
    path('', views.all_lessons, name='all_lessons'),
    path('<lesson_id>/', views.lesson_detail, name='lesson_detail'),
]
