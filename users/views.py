from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import User

def register_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, "Пароли не совпадают")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email уже используется")
        else:
            user = User.objects.create_user(email=email, username=username, password=password)
            messages.success(request, "Аккаунт создан")
            return redirect('login')

    return render(request, 'auth/register.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, "Неверный email или пароль")

    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')
