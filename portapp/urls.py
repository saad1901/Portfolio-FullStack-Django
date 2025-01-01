from django.contrib import admin
from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('saadadmin/', admin.site.urls),
    path('adminpanel/', views.adminpanel, name='adminpanel'),
    path('', views.home, name='home'),
    path('login', views.admin, name='login'),
    path('admin', views.homepage, name='admin'), 
    path('admin/details', views.details, name='details'),
    path('admin/resume', views.resume, name='resume'),
    path('project/blog', views.blog, name='blog'),
    path('<str:username>/', views.portfolio, name='portfolio'),
    path('project/<int:pid>/', views.project, name='project'),
    path('paynow', views.paynow, name='paynow'), 
    path('signup', views.signup, name='signup'),    
    path('logout', views.logoutuser, name='logout'), 
    path('projects', views.projects, name='projects'), 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)