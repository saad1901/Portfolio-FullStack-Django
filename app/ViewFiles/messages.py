from django.shortcuts import render,redirect
from app.models import Message
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def messagesto(request):
    messages = Message.objects.filter(to=request.user).order_by('-time')
    return render(request, 'user/messages/messages.html', {'allmsgs': messages})

@login_required
def delete_message(request, id):
    try:
        message = Message.objects.get(id=id, to=request.user)
        message.delete()
        messages.success(request, "Message deleted successfully.")
        return redirect('messages')
    except Message.DoesNotExist:
        messages.error(request, "Message not found or you do not have permission to delete it.")
        return redirect('messages')