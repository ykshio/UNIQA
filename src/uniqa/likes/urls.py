
# likes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('add/<int:content_id>/', views.like_add_view, name='like_add'),
    path('remove/<int:content_id>/', views.like_remove_view, name='like_remove'),
]
