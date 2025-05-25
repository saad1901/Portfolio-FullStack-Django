from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Info, Education
from app.forms import UserDetailsForm, InfoForm, EducationForm
from django.contrib.auth.decorators import login_required
import datetime

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
                if request.FILES.get('img'):
                    user.image = request.FILES.get('img')
                    user.save()
                    # get_trans_image(user.image, user.username + '.png')
                if request.FILES.get('resume'):
                    user.resume = request.FILES.get('resume')
                    user.save()
            else:
                messages.success(request, details_form.errors)
                print(details_form.errors)

        if 'add-info' in request.POST:
            print('info_form')
            action = request.POST.get('info_form')
            new_info_form = InfoForm(request.POST)
            if new_info_form.is_valid():
                print('new_info_form')
                new_info_instance = new_info_form.save(commit=False)
                new_info_instance.fk_id = user.id
                new_info_instance.save()

        elif 'del-info' in request.POST:

            i_id = request.POST.get('del-info')
            infos = get_object_or_404(Info, id=i_id, fk=user)
            infos.delete()
            return redirect('details')
        messages.success(request, "Your details have been updated successfully!")
        return redirect('details')
    
    details_form = UserDetailsForm(instance=user)
    edu_form = [EducationForm(instance=i) for i in edudata]

    return render(request, 'user/details/detail.html', {
        'user': user,
        'details_form': details_form,
        'info_forms': info,
        'edu_form': edu_form,
        'def_date': datetime.date(2001, 1, 1)
    })

