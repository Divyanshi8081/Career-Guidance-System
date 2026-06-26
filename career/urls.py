from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('quiz/', views.quiz_view, name='quiz'),
    path('quiz/result/<int:pk>/', views.quiz_result_view, name='quiz_result'),
    path('skill-gap/', views.skill_gap_view, name='skill_gap'),
]
