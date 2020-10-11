"""testdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include
from user.views import home

# add from ko
from django.conf import settings
from django.conf.urls.static import static
from user import views

app_name = 'testdb'
urlpatterns = [
    path('user/', include('user.urls')),
    path('admin/', admin.site.urls),
    path('',home, name='home'),
    path('files/', views.file_list, name='file_list'),
    path('files/upload/', views.upload_file, name='upload_file'),
    path('user/login/' , views.login, name='login'),
    path('user/logout/', views.logout, name='logout'),
    path('user/register/', views.register, name='register'),
    path('user/<int:pk>/invite/' , views.invite, name='invite'),
    path('user/room_list/' , views.room_list, name='room_list'),
    path('user/make_room/' , views.make_room, name='make_room'),    
    path('user/index/' , views.index, name='index'),    
    path('user/join/' , views.join, name='join'),   
    path('<int:pk>/update/', views.FileUpdateView.as_view, name='update'),
    path('index/<int:pk>/room_delete/', views.room_delete, name='room_delete'), 
    path('index/<int:pk>/room_exit/', views.room_exit, name='room_exit'), 
    path('index/<int:pk>/join/', views.room_join, name='room_join'),  
    path('index/<int:pk>/invite/', views.student_invite, name='student_invite'),
    path('modal/', views.modal , name='modal'),
    path('files/<int:pk>/room_choice', views.room_choice , name='room_choice'),
    path('test/', views.test , name='test'),
    path('index/<int:pk>/file_delete/', views.file_delete, name='file_delete'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
