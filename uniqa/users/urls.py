
# users/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import CustomLogoutView

app_name = 'users'

urlpatterns = [
    path('signup/', views.signup_request, name='signup'),
    path('signup/<str:token>/', views.signup_confirm, name='signup_confirm'),
    path('profile/<int:pk>/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.profile_edit_view, name='profile_edit'),
    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),  # ログイン
    path('logout/', LogoutView.as_view(next_page='home'), name='logout'),
]
