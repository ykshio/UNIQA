# questions/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('new/', views.question_create, name='question_create'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
]

