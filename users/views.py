from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from users.models import Score
from users.models import UserProgress


# Create your views here.

def register_handler(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        user = User.objects.create_user(username, email=email, password=password)
        user.save()
        return redirect('/login')
    else:
        return render(request, 'register.html')


def login_handler(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/user')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def logout_handler(request):
    logout(request)
    return redirect("/login")


@login_required(login_url='/login')
def user_handler(request):
    user = User.objects.get(username=request.user.username)
    if request.method == 'POST':
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
    user = User.objects.get(username=request.user.username)

    user_score = Score.objects.filter(user=user)
    if not user_score:
        user_score = Score(user=user, score=0)
        user_score.save()

    return render(request, 'user-profile.html', {'user': user, 'user_score': user_score})


def user_delete_handler(request):
    return HttpResponse("delete user")
