from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def all_lessons(request):
    return HttpResponse("all lessons")


def lesson_detail(request, lesson_id):
    return HttpResponse("lesson detail: {{lesson_id}}")
