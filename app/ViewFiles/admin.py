from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from app.models import CustomUser, Info, Education, Experience, Skill, Projects,News, Message
from app.forms import UserDetailsForm, InfoForm, EducationForm, SignupForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.forms import modelformset_factory
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import datetime
import pytz
import requests

def is_superuser(user):
    return user.is_superuser

@csrf_exempt
def adminpanel(request):
    if request.user.is_authenticated and request.user.username == 'adminsaad':
        if request.method == 'POST':
            if 'user_id' in request.POST:  # Handling user status update
                print('user_id')
                user_id = request.POST.get('user_id')
                # new_status = request.POST.get('status')
                try:
                    user = CustomUser.objects.get(id=user_id)
                    if user.paid:
                        user.paid = False
                    else:
                        user.paid = True
                    user.save()
                except CustomUser.DoesNotExist:
                    pass

            elif 'addnews' in request.POST: 
                print('addnews')
                head = request.POST.get('head')
                body = request.POST.get('body')
                IST = pytz.timezone('Asia/Kolkata')
                current_time_ist = timezone.now().astimezone(IST)
                news = News(head=head, body=body, timex=current_time_ist)
                news.save()
                messages.success(request, "News added successfully.")

            elif 'delete_news_id' in request.POST:
                news_id = request.POST.get('delete_news_id')
                news = get_object_or_404(News, id=news_id)
                news.delete()
                messages.success(request, "News deleted successfully.")

            elif "delete_user_id" in request.POST:
                user_id = request.POST.get("delete_user_id")
                user_to_delete = CustomUser.objects.get(id=user_id)
                user_to_delete.delete()
                messages.success(request, "User deleted successfully.")
            return redirect('adminpanel')
            

        users = CustomUser.objects.all()
        all_news = News.objects.all().order_by('timex')
        return render(request, 'admin/Dashboard/dashboard.html', {'users': users, 'all_news':all_news})

    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            if username == 'adminsaad':
                password = request.POST.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return redirect('adminpanel')
                else:
                    return render(request, 'adminlogin.html', {'error': 'Invalid username or password'})
            else:
                return HttpResponse('Login failed as Admin, Maybe You are not the one as expected')
        total = len(CustomUser.objects.all())
        print(total)
        return render(request, 'admin/Auth/adminlogin.html', {'total':total})

@login_required
def admindetail(request, user_id):
    if request.user.username == 'adminsaad':
        user = CustomUser.objects.get(id=user_id)
        info = Info.objects.filter(fk_id=user_id)
        education = Education.objects.filter(fk_id=user_id)
        experience = Experience.objects.filter(fk_id=user_id)
        projects = Projects.objects.filter(fk_id=user_id)
        skills = Skill.objects.filter(fk_id=user_id)
    else:
        redirect('admin')


@login_required
def users(request):
    users = CustomUser.objects.all()
    return render(request, 'admin/User/user_management.html', {'users': users})

@login_required
def news(request):
    all_news = News.objects.all().order_by('timex')
    return render(request, 'admin/News/news_management.html', {'all_news':all_news})