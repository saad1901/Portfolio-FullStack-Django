from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('admin')
    return render(request, 'site/site.html')