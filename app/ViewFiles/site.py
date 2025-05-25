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

def home(request):
    if request.user.is_authenticated:
        return redirect('admin')
    return render(request, 'site.html')