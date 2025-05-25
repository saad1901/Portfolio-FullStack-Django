from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from app.models import CustomUser, Info, Education, Experience, Skill, Projects,News, Message
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

def portfolio(request, username):
    try:
        if request.method == 'POST' and 'sendmsg' in request.POST:
            print('caleed portfolio')
            fullname = request.POST.get('fullname')
            email = request.POST.get('email')
            message = request.POST.get('message')
            Message.objects.create(
                fullname=fullname,
                email=email,
                message=message,
                to=CustomUser.objects.get(username=username)
            )
            messages.success(request, "Message sent successfully!")
            return redirect('portfolio', username=username)    
        
        user = CustomUser.objects.get(username=username)
        if not user:
            return HttpResponse("User not found.", status=404)

        if user.paid == False:
            return render(request, 'user/payment/notpaid.html', {'user': user})

        info = Info.objects.filter(fk_id=user.id)
        edudata = Education.objects.filter(fk_id=user.id)
        experiences = Experience.objects.filter(fk=user)
        skills = Skill.objects.filter(fk=user)
        projects = Projects.objects.filter(fk=user)
        context={'user': user, 'info': info, 'edudata': edudata,
                 'experiences': experiences, 'skills': skills,
                 'projects': projects}

        if user.theme == 1 or user.theme == 2:
            return render(request, 'user/portfolios/index.html', context)
        elif user.theme == 4:
            return render(request, 'user/portfolios/theme4/index.html', context)
        else:
            return render(request, 'user/portfolios/index3.html', context)
            
    except Exception as e:
        return HttpResponse(f"Something went wrong: {str(e)}", status=500)