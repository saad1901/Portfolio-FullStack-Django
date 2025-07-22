from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import News
from django.contrib.auth.decorators import login_required

@login_required
def homepage(request):
    if request.method == 'POST':
        theme_choice = request.POST.get('theme')
        if theme_choice and theme_choice.isdigit():
            try:
                # Convert theme choice to an integer and validate against the defined choices
                theme_choice = int(theme_choice)
                if theme_choice:
                    request.user.theme = theme_choice
                    request.user.save()
                    messages.success(request, "Your theme has been updated successfully!")
                else:
                    messages.error(request, "Invalid theme selection.")
            except ValueError:
                messages.error(request, "Invalid input for theme selection.")
        else:
            messages.error(request, "Theme selection is required.")
        return redirect('admin')
    news = News.objects.all().order_by('-timex')
    return render(request, 'user/dashboard/homepage.html', {'news':news})