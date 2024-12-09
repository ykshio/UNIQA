# questions/urls.py
from django.urls import path, include
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('users/', include('users.urls')),
    path('new/', views.question_create, name='question_create'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('question_form/', views.question_form, name='question_form'),
]

