from django.shortcuts import render
from app.models import Message
from django.contrib.auth.decorators import login_required

@login_required
def messagesto(request):
    messages = Message.objects.filter(to=request.user).order_by('-time')
    return render(request, 'user/messages/messages.html', {'messages': messages})
