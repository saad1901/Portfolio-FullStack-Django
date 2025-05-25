from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import CustomUser
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password

def loginuser(request):
    if request.user.is_authenticated:
        return redirect('admin')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            CustomUser.objects.get(username=username)
        except:
            return render(request, 'user/auth/login.html', {'message': 'Invalid username'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            context = {'message': 'Invalid Password'}
            return render(request, 'user/auth/login.html', context)
    return render(request, 'user/auth/login.html')

@login_required
def logoutuser(request):
    logout(request)
    return redirect('login')

def signup(request):
    if request.method == 'POST':
        data = request.POST
        if data['password1'] != data['password2']:
            messages.error(request, "Passwords do not match.")
            return redirect('signup')
        
        if CustomUser.objects.filter(username=data['username']).exists():
            messages.error(request, "Username already exists.")
            return redirect('signup')
        
        if CustomUser.objects.filter(email=data['email']).exists():
            messages.error(request, "Email already exists.")
            return redirect('signup')

        CustomUser.objects.create(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            password=make_password(data['password1']),  # Hash password
        )   
        user = authenticate(request, username=data['username'], password=data['password1'])
        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            messages.error(request, "Authentication failed.")
            return redirect('signup')

    return render(request, 'user/auth/signup.html')