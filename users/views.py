from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from users.forms import RegisterUserForm, LoginUserForm
from users.models import Score


def register_handler(request):
    if request.method == 'GET':
        user_registration_form = RegisterUserForm()
        return render(request, 'register.html', {'user_registration_form': user_registration_form})

    if request.method == 'POST':
        register_user_form = RegisterUserForm(request.POST)
        if register_user_form.is_valid():
            user = register_user_form.save(commit=False)  # Don't save yet
            password = register_user_form.cleaned_data.get('password')
            user.set_password(password)  # Hash the password
            user.save()  # Save the user with hashed password
            return redirect('/login')
        else:
            return render(request, 'register.html', {'user_registration_form': register_user_form})


def login_handler(request):
    if request.method == 'GET':
        user_login_form = LoginUserForm()
        return render(request, 'login.html', {'user_login_form': user_login_form})
    if request.method == 'POST':
        user_login_form = LoginUserForm(request.POST)
        user = authenticate(request, username=user_login_form.data.get('username'),
                            password=user_login_form.data.get('password'))
        if user is not None:
            login(request, user)
            return redirect('/user')
        return render(request, 'login.html',
                      {'error': 'Invalid username or password', 'user_login_form': user_login_form})


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
