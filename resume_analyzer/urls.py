from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_resume, name='upload_resume'),
    path('result/<int:pk>/', views.resume_result, name='resume_result'),
    path('list/', views.resume_list, name='resume_list'),
    path('delete/<int:pk>/', views.delete_resume, name='delete_resume'),
]
