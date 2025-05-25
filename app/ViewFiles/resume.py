from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from app.models import Education, Experience, Skill
from django.contrib.auth.decorators import login_required

@login_required
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
            messages.success(request, "Education deleted successfully.")
            # return redirect('resume')
        elif 'delete_experience' in request.POST:
            experience_id = request.POST.get('delete_experience')
            experience = get_object_or_404(
                Experience, id=experience_id, fk=user)
            experience.delete()
            messages.success(request, "Experience deleted successfully.")
            # return redirect('resume')
        elif 'delete_skill' in request.POST:
            skill_id = request.POST.get('delete_skill')
            skill = get_object_or_404(Skill, id=skill_id, fk=user)
            skill.delete()
            messages.success(request, "Skill deleted successfully.")
            # return redirect('resume')

        if 'add_education' in request.POST:
            name = request.POST.get('education_name')
            yearfrom = request.POST.get('education_yearfrom')
            yearto = request.POST.get('education_yearto')
            about = request.POST.get('education_about')
            Education.objects.create(
                fk=user, name=name, yearfrom=yearfrom, yearto=yearto, about=about)
            messages.success(request, "Education added successfully.")
            # return redirect('resume')
        elif 'add_experience' in request.POST:
            name = request.POST.get('experience_name')
            yearfrom = request.POST.get('experience_yearfrom')
            yearto = request.POST.get('experience_yearto')
            role = request.POST.get('experience_role')
            Experience.objects.create(
                fk=user, name=name, yearfrom=yearfrom, yearto=yearto, role=role)
            messages.success(request, "Experience added successfully.")
            # return redirect('resume')
        elif 'add_skill' in request.POST:
            name = request.POST.get('skill_name')
            percentage = request.POST.get('skill_percentage')
            Skill.objects.create(fk=user, name=name, percentage=percentage)
            messages.success(request, "Skill added successfully.")
        return redirect('resume')

    return render(request, 'user/resume/resume.html', {
        'educations': educations,
        'experiences': experiences,
        'skills': skills,
    })