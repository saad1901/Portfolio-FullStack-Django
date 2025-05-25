from django.contrib import admin
from django.urls import path, include
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
    path('', include('app.urls'))
    # path('api/alldetails' , views.UserDetails.as_view()), 
    # path('api/alldetails/<int:pk>' , views.UserDetail.as_view()) ,
    # path('api/data' , views.GetData.as_view()), 
    # path('api/data/<int:pk>' , views.GetDatabyID.as_view()) 

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)