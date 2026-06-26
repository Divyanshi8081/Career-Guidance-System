from django.urls import path
from . import views

urlpatterns = [
    path('', views.chatbot_view, name='chatbot'),
    path('new/', views.new_session, name='new_chat'),
    path('delete/<int:pk>/', views.delete_session, name='delete_chat'),
    path('api/chat/', views.chat_api, name='chat_api'),
]
