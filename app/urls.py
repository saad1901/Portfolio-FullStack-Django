from django.contrib import admin
from django.urls import path
from app.ViewFiles import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('adminpanel/', adminpanel, name='adminpanel'),
    path('', home, name='home'),
    path('login', loginuser, name='login'),
    path('admin', homepage, name='admin'), 
    path('admin/details', details, name='details'),
    path('admin/resume', resume, name='resume'),
    path('project/blog', blog, name='blog'),
    path('<str:username>/', portfolio, name='portfolio'),
    path('project/<int:pid>/', project, name='project'),
    path('paynow', paynow, name='paynow'), 
    path('signup', signup, name='signup'),    
    path('logout', logoutuser, name='logout'), 
    path('admin/projects', projects, name='projects'),
    path('admin/messages', messagesto, name='messages'),
    path('admin/messages/deletemsg/<int:id>', delete_message, name='delete_message'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)