from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from app.models import CustomUser, Info, Education, Experience, Skill, Projects,News
from .forms import UserDetailsForm, InfoForm, EducationForm, SignupForm
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
# from rest_framework import response, mixins, generics, viewsets
# from .serializer import UserSrlz
# from rest_framework.authentication import BasicAuthentication
# from  rest_framework.permissions import IsAuthenticated

def is_superuser(user):
    return user.is_superuser

# class UserDetails(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSrlz

#     def get(self, request):
#         return self.list(request)
    
#     def post(self, request):
#         return self.create(request)

# class UserDetail(mixins.RetrieveModelMixin,mixins.UpdateModelMixin, mixins.DestroyModelMixin, generics.GenericAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSrlz

#     def get(self, request, pk):
#         return self.retrieve(request,pk)
    
#     def put(self, request, pk):
#         return self.update(request,pk)

#     def delete(self, request, pk):
#         return self.destroy(request,pk)

# class GetData(generics.ListCreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSrlz

# class GetDatabyID(generics.RetrieveUpdateDestroyAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSrlz


# class GetTheData(viewsets.ModelViewSet):
#     queryset = CustomUser.objects.all()
#     serializer_class = UserSrlz
    # authentication_classes = [BasicAuthentication] # we dont need this if we use token based authn at global level
    # permission_classes = [IsAuthenticated]


## API SECTION ENDS HERE ##

@login_required
def logoutuser(request):
    logout(request)
    return redirect('login')

def signup(request):
    # test
    if request.method == 'POST':
        data = request.POST
        if data['password1'] != data['password2']:
            messages.error(request, "Passwords do not match.")
            return render(request, 'signup.html')
        
        if CustomUser.objects.filter(username=data['username']).exists():
            messages.error(request, "Username already exists.")
            return render(request, 'signup.html')
        
        if CustomUser.objects.filter(email=data['email']).exists():
            messages.error(request, "Email already exists.")
            return render(request, 'signup.html')

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
            return render(request, 'signup.html')

    return render(request, 'signup.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('admin')
    return render(request, 'site.html')


def admin(request):
    if request.user.is_authenticated:
        return redirect('admin')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            CustomUser.objects.get(username=username)
        except:
            return render(request, 'login.html', {'message': 'Invalid username'})

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('admin')
        else:
            context = {'message': 'Invalid Password'}
            return render(request, 'login.html', context)
    return render(request, 'login.html')


def portfolio(request, username):
    try:
        user = CustomUser.objects.get(username=username)
        if not user:
            return HttpResponse("User not found.", status=404)

        if user.paid == False:
            return render(request, 'notpaid.html', {'user': user})

        info = Info.objects.filter(fk_id=user.id)
        edudata = Education.objects.filter(fk_id=user.id)
        experiences = Experience.objects.filter(fk=user)
        skills = Skill.objects.filter(fk=user)
        projects = Projects.objects.filter(fk=user)
        context={'user': user, 'info': info, 'edudata': edudata,
                 'experiences': experiences, 'skills': skills,
                 'projects': projects}

        if user.theme == 1 or user.theme == 2:
            return render(request, 'index.html', context)
        else:
            return render(request, 'index3.html', context)
            
    except Exception as e:
        return HttpResponse(f"Something went wrong: {str(e)}", status=500)


def paynow(request):
    pass


@login_required
def details(request):
    user = request.user
    info = Info.objects.filter(fk_id=user.id)
    edudata = Education.objects.filter(fk_id=user.id)

    if request.method == 'POST':

        if 'details_forms' in request.POST:

            details_form = UserDetailsForm(request.POST, instance=user)
            if details_form.is_valid():

                details_instance = details_form.save(commit=False)
                details_instance.save()
            else:
                print(details_form.errors)

        if 'info_form' in request.POST:

            action = request.POST.get('info_form')
            if action == 'add_new_info':

                new_info_form = InfoForm(request.POST)
                if new_info_form.is_valid():

                    new_info_instance = new_info_form.save(commit=False)
                    new_info_instance.fk_id = user.id
                    new_info_instance.save()
                    return redirect('details')

        elif 'del-info' in request.POST:

            i_id = request.POST.get('del-info')
            infos = get_object_or_404(Info, id=i_id, fk=user)
            infos.delete()
            return redirect('details')

    details_form = UserDetailsForm(instance=user)
    edu_form = [EducationForm(instance=i) for i in edudata]

    return render(request, 'detail.html', {
        'user': user,
        'details_form': details_form,
        'info_forms': info,
        'edu_form': edu_form,
        'def_date': datetime.date(2001, 1, 1)
    })


@login_required
def homepage(request):
    if request.method == 'POST':
        print(1)
        theme_choice = request.POST.get('theme')
        if theme_choice and theme_choice.isdigit():
            print(2)
            try:
                # Convert theme choice to an integer and validate against the defined choices
                theme_choice = int(theme_choice)
                if theme_choice in dict(request.user.ThemeChoices.choices).keys():
                    request.user.theme = theme_choice
                    request.user.save()
                    messages.success(
                        request, "Your theme has been updated successfully!")
                else:
                    messages.error(request, "Invalid theme selection.")
            except ValueError:
                messages.error(request, "Invalid input for theme selection.")
        else:
            messages.error(request, "Theme selection is required.")
    news = News.objects.all()
    return render(request, 'homepage.html', {'news':news})


@login_required
# @user_passes_test(is_superuser)
def resume(request):
    user = request.user
    # Fetch all education, experience, and skills entries for the logged-in user
    educations = Education.objects.filter(fk=user)
    experiences = Experience.objects.filter(fk=user)
    skills = Skill.objects.filter(fk=user)

    if request.method == 'POST':
        # Handle deletion of entries
        if 'delete_education' in request.POST:
            education_id = request.POST.get('delete_education')
            education = get_object_or_404(Education, id=education_id, fk=user)
            education.delete()
            return redirect('resume')
        elif 'delete_experience' in request.POST:
            experience_id = request.POST.get('delete_experience')
            experience = get_object_or_404(
                Experience, id=experience_id, fk=user)
            experience.delete()
            return redirect('resume')
        elif 'delete_skill' in request.POST:
            skill_id = request.POST.get('delete_skill')
            skill = get_object_or_404(Skill, id=skill_id, fk=user)
            skill.delete()
            return redirect('resume')

        if 'add_education' in request.POST:
            name = request.POST.get('education_name')
            yearfrom = request.POST.get('education_yearfrom')
            yearto = request.POST.get('education_yearto')
            about = request.POST.get('education_about')
            Education.objects.create(
                fk=user, name=name, yearfrom=yearfrom, yearto=yearto, about=about)
            return redirect('resume')
        elif 'add_experience' in request.POST:
            name = request.POST.get('experience_name')
            yearfrom = request.POST.get('experience_yearfrom')
            yearto = request.POST.get('experience_yearto')
            role = request.POST.get('experience_role')
            Experience.objects.create(
                fk=user, name=name, yearfrom=yearfrom, yearto=yearto, role=role)
            return redirect('resume')
        elif 'add_skill' in request.POST:
            name = request.POST.get('skill_name')
            percentage = request.POST.get('skill_percentage')
            Skill.objects.create(fk=user, name=name, percentage=percentage)
            return redirect('resume')

    return render(request, 'resume.html', {
        'educations': educations,
        'experiences': experiences,
        'skills': skills,
    })


@login_required
def projects(request):
    user = request.user
    projects = Projects.objects.filter(fk=user)
    if request.method == 'POST':
        if 'add_project' in request.POST:
            name = request.POST.get('name')
            techused = request.POST.get('techused')
            description = request.POST.get('description')
            image = request.FILES.get('image')
            Projects.objects.create(
                fk=user, name=name, techused=techused, description=description, image=image)
            return redirect('projects')

        elif 'delete_project_id' in request.POST:
            project_id = request.POST.get('delete_project_id')
            project = get_object_or_404(Projects, id=project_id, fk=user)
            project.delete()
            return redirect('projects')

    return render(request, 'projects.html', {'user': user, 'projects': projects})


def project(request, pid):
    try:

        project = Projects.objects.get(id=pid)

        user = CustomUser.objects.get(id=project.fk_id)

        user_projects = Projects.objects.filter(
            fk_id=project.fk_id).order_by('id')
        project_ids = list(user_projects.values_list('id', flat=True))

        current_index = project_ids.index(project.id)

        next_project = project_ids[(current_index + 1) % len(project_ids)]
        previous_project = project_ids[current_index -
                                       1] if current_index > 0 else project_ids[-1]

        return render(request, 'project.html', {
            'project': project,
            'user': user,
            'next_project': next_project,
            'previous_project': previous_project
        })

    except Projects.DoesNotExist:
        return HttpResponse("Project not found.", status=404)
    except CustomUser.DoesNotExist:
        return HttpResponse("User not found.", status=404)
    except Exception as e:
        return HttpResponse(f"An error occurred: {str(e)}", status=500)



@csrf_exempt
def adminpanel(request):
    if request.user.is_authenticated and request.user.username == 'adminsaad':

        if request.method == 'POST':
            if 'user_id' in request.POST:  # Handling user status update
                user_id = request.POST.get('user_id')
                new_status = request.POST.get('status')
                try:
                    user = CustomUser.objects.get(id=user_id)
                    user.paid = new_status
                    user.save()
                except CustomUser.DoesNotExist:
                    pass
                return redirect('adminpanel')

            elif 'head' in request.POST and 'body' in request.POST: 
                head = request.POST.get('head')
                body = request.POST.get('body')
                IST = pytz.timezone('Asia/Kolkata')
                current_time_ist = timezone.now().astimezone(IST)
                news = News(head=head, body=body, timex=current_time_ist)
                news.save()
                print(current_time_ist)
                return redirect('adminpanel')

            elif 'delete_news_id' in request.POST:
                news_id = request.POST.get('delete_news_id')
                news = get_object_or_404(News, id=news_id)
                news.delete()


            elif "delete_user_id" in request.POST:
                user_id = request.POST.get("delete_user_id")
                user_to_delete = CustomUser.objects.get(id=user_id)
                user_to_delete.delete()
            

        users = CustomUser.objects.all()
        news = News.objects.all()
        return render(request, 'adminpanel.html', {'users': users, 'news':news})

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
        return render(request, 'adminlogin.html', {'total':total})


@login_required
def blog(request):
    return render(request, 'blog.html')


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