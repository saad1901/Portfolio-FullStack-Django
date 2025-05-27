from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib import messages
from app.models import CustomUser, Projects
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage

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
            github = request.POST.get('github')
            link = request.POST.get('link')
            
            Projects.objects.create(
                fk=user, name=name, techused=techused, description=description, image=image, github=github, link=link)
            # return redirect('projects')
            messages.success(request, "Project added successfully.")

        elif 'delete_project_id' in request.POST:
            project_id = request.POST.get('delete_project_id')
            project = get_object_or_404(Projects, id=project_id, fk=user)
            if project.image:
                try:
                    default_storage.delete(project.image.path)
                except:
                    pass
            project.delete()
            messages.success(request, "Project deleted successfully.")
        return redirect('projects')

    return render(request, 'user/projects/projects.html', {'user': user, 'projects': projects})

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

        return render(request, 'user/projects/project.html', {
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
