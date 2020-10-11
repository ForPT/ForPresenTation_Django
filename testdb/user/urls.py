from django.urls import path
from user import views

app_name = 'user' 

urlpatterns = [

    path('', views.FileLV.as_view(), name='test'),
    path('<int:pk>/', views.FileDV.as_view(), name='detail'),
    path('<int:pk>/delete', views.FileDeleteView.as_view(), name='delete'),
    path('<int:pk>/update/',
         views.FileUpdateView.as_view(), name="update"),
         
    #add from ko
]