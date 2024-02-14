from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.

def register_handler(request):
    return HttpResponse("register")


def login_handler(request):
    return HttpResponse("login")


def logout_handler(request):
    return HttpResponse("logout")


def user_handler(request):
    return HttpResponse("user")


def user_delete_handler(request):
    return HttpResponse("delete user")
