
# polls/urls.py
from django.urls import path
from . import views

app_name = 'polls'

urlpatterns = [
    path('', views.poll_list, name='poll_list'),
    path('new/', views.poll_create, name='poll_create'),
    path('<int:pk>/', views.poll_detail, name='poll_detail'),
]
