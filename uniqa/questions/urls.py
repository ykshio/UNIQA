# questions/urls.py
from django.urls import path, include
from . import views

app_name = 'questions'

urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('users/', include('users.urls')),
    path('new/', views.question_create, name='question_create'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('<int:question_id>/toggle_resolution/', views.toggle_resolution, name='toggle_resolution'),
    path('question_form/', views.question_form, name='question_form'),
    path('<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('answers/<int:answer_id>/delete/', views.delete_answer, name='delete_answer'),
    path('answers/<int:answer_id>/like/', views.like_answer, name='like_answer'),

]

