from django.contrib import admin
from django.urls import path, include
from app import views
from django.conf import settings
from django.conf.urls.static import static
# from rest_framework.routers import DefaultRouter
# from rest_framework.authtoken.views import obtain_auth_token

# router = DefaultRouter()
# router.register('api/viewsetdata', views.GetTheData)

# urlpatterns = [
#     path('' , include(router.urls)),
#     path('gettoken',obtain_auth_token, name='gettoken'),
#     path('login', views.admin, name='login'),
# ]

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
    path('admin/projects', views.projects, name='projects'),
    path('admin/messages', views.messagesto, name='messages'),
    # path('api/alldetails' , views.UserDetails.as_view()), 
    # path('api/alldetails/<int:pk>' , views.UserDetail.as_view()) ,
    # path('api/data' , views.GetData.as_view()), 
    # path('api/data/<int:pk>' , views.GetDatabyID.as_view()) 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)